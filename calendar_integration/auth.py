"""
Аутентификация и управление токенами для Google Calendar API.

Предоставляет:
    - CalendarAuth: основной класс для OAuth flow и управления credentials
    - SecureTokenStorage: шифрованное хранилище токенов через Fernet
    - Декоратор require_auth для методов, требующих авторизации

Поток аутентификации:
    1. Проверка наличия сохранённых зашифрованных credentials
    2. Если нет — запуск OAuth flow через локальный сервер
    3. Автоматический refresh токена при истечении
    4. Шифрование и сохранение через Fernet

Примеры:
    >>> auth = CalendarAuth(
    ...     client_secrets_file="credentials.json",
    ...     encryption_key="my-secret-key"
    ... )
    >>> creds = auth.authenticate()
    >>> service = build("calendar", "v3", credentials=creds)
"""

from __future__ import annotations

import base64
import json
import logging
import os
import pickle
import random
import time
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

from .config import (
    DEFAULT_SCOPES,
    GOOGLE_TOKEN_URI,
    MAX_RETRIES,
    BASE_RETRY_DELAY,
    MAX_RETRY_DELAY,
    RETRYABLE_STATUS_CODES,
)
from .exceptions import (
    AuthError,
    CredentialsNotFoundError,
    MaxRetriesExceededError,
    RateLimitError,
    TokenExpiredError,
    TokenRefreshError,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Secure Token Storage с Fernet шифрованием
# ---------------------------------------------------------------------------


class SecureTokenStorage:
    """
    Шифрованное хранилище токенов на основе Fernet (AES-128-CBC + HMAC).

    Шифрует pickle-данные credentials перед сохранением на диск.
    Ключ шифрования выводится из пользовательского пароля через PBKDF2.

    Attributes:
        _cipher: Экземпляр Fernet для шифрования/дешифрования.
        _storage_dir: Директория для хранения зашифрованных файлов.

    Example:
        >>> storage = SecureTokenStorage(encryption_key="my-secret-password")
        >>> storage.store(credentials, "/tmp/tokens/creds.enc")
        >>> loaded = storage.load("/tmp/tokens/creds.enc")
    """

    _SALT_LENGTH: int = 16
    _ITERATIONS: int = 100_000

    def __init__(self, encryption_key: str, storage_dir: Optional[str] = None) -> None:
        """
        Инициализировать хранилище.

        Args:
            encryption_key: Пароль для шифрования (будет использован для
                вывода ключа через PBKDF2).
            storage_dir: Директория для хранения файлов. По умолчанию ~/.calendar_tokens.
        """
        self._cipher = self._create_cipher(encryption_key)
        self._storage_dir = Path(storage_dir or os.path.expanduser("~/.calendar_tokens"))
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("Инициализировано хранилище токенов: %s", self._storage_dir)

    def _create_cipher(self, password: str) -> Fernet:
        """
        Создать Fernet cipher из пароля через PBKDF2.

        Args:
            password: Пользовательский пароль.

        Returns:
            Экземпляр Fernet для шифрования.
        """
        # Используем случайный salt, сохраняемый рядом с зашифрованными данными
        salt_file = self._storage_dir / ".salt"
        if salt_file.exists():
            salt = salt_file.read_bytes()
        else:
            salt = os.urandom(16)
            salt_file.write_bytes(salt)
            os.chmod(salt_file, 0o600)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self._ITERATIONS,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))
        return Fernet(key)

    def store(self, credentials: Credentials, file_path: Optional[str] = None) -> Path:
        """
        Зашифровать и сохранить credentials на диск.

        Args:
            credentials: Google OAuth2 Credentials для сохранения.
            file_path: Путь к файлу. По умолчанию {storage_dir}/credentials.enc.

        Returns:
            Путь к сохранённому файлу.
        """
        path = Path(file_path) if file_path else self._storage_dir / "credentials.enc"
        try:
            # Сериализуем credentials через pickle
            pickled: bytes = pickle.dumps(credentials)
            # Шифруем
            encrypted: bytes = self._cipher.encrypt(pickled)
            # Сохраняем
            path.write_bytes(encrypted)
            # Устанавливаем restrictive permissions (только владелец)
            os.chmod(path, 0o600)
            logger.info("Credentials зашифрованы и сохранены: %s", path)
            return path
        except Exception as exc:
            logger.error("Ошибка при сохранении credentials: %s", exc)
            raise AuthError(f"Не удалось сохранить credentials: {exc}") from exc

    def load(self, file_path: Optional[str] = None) -> Credentials:
        """
        Загрузить и расшифровать credentials с диска.

        Args:
            file_path: Путь к файлу. По умолчанию {storage_dir}/credentials.enc.

        Returns:
            Расшифрованные Google OAuth2 Credentials.

        Raises:
            CredentialsNotFoundError: Если файл не существует.
            AuthError: Если не удалось расшифровать или десериализовать.
        """
        path = Path(file_path) if file_path else self._storage_dir / "credentials.enc"
        if not path.exists():
            raise CredentialsNotFoundError(
                f"Файл credentials не найден: {path}"
            )

        try:
            encrypted: bytes = path.read_bytes()
            pickled: bytes = self._cipher.decrypt(encrypted)
            credentials: Credentials = pickle.loads(pickled)
            logger.info("Credentials загружены из: %s", path)
            return credentials
        except CredentialsNotFoundError:
            raise
        except Exception as exc:
            logger.error("Ошибка при загрузке credentials: %s", exc)
            raise AuthError(
                f"Не удалось расшифровать credentials (возможно, неверный ключ): {exc}"
            ) from exc

    def exists(self, file_path: Optional[str] = None) -> bool:
        """Проверить, существует ли файл с зашифрованными credentials."""
        path = Path(file_path) if file_path else self._storage_dir / "credentials.enc"
        return path.exists()

    def delete(self, file_path: Optional[str] = None) -> None:
        """Удалить файл с зашифрованными credentials."""
        path = Path(file_path) if file_path else self._storage_dir / "credentials.enc"
        if path.exists():
            path.unlink()
            logger.info("Файл credentials удалён: %s", path)


# ---------------------------------------------------------------------------
# Декоратор для методов, требующих авторизации
# ---------------------------------------------------------------------------


F = Callable[..., Any]


def require_auth(method: F) -> F:
    """
    Декоратор: проверяет аутентификацию перед вызовом метода.

    Если credentials не инициализированы — вызывает authenticate().
    Если токен истёк — вызывает refresh_if_needed().

    Args:
        method: Метод, требующий авторизации.

    Returns:
        Обернутый метод с автоматической проверкой авторизации.
    """
    @wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        if not hasattr(self, "_credentials") or self._credentials is None:
            logger.debug("Credentials не инициализированы, запускаем authenticate()")
            self.authenticate()
        if hasattr(self, "refresh_if_needed"):
            self.refresh_if_needed()
        return method(self, *args, **kwargs)
    return wrapper  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Основной класс аутентификации
# ---------------------------------------------------------------------------


class CalendarAuth:
    """
    Управление аутентификацией Google Calendar API.

    Обрабатывает полный OAuth flow, автоматический refresh токена
    и безопасное хранение credentials через Fernet-шифрование.

    Attributes:
        _client_secrets_file: Путь к JSON-файлу с client secrets.
        _scopes: Список OAuth scopes.
        _storage: Экземпляр SecureTokenStorage для шифрованного хранения.
        _credentials: Текущие Google OAuth2 Credentials.

    Example:
        >>> auth = CalendarAuth(
        ...     client_secrets_file="credentials.json",
        ...     encryption_key="my-secret-password",
        ... )
        >>> creds = auth.authenticate()
        >>> # ... использование creds ...
        >>> auth.refresh_if_needed()  # автоматический refresh
    """

    def __init__(
        self,
        client_secrets_file: str = "credentials.json",
        encryption_key: Optional[str] = None,
        scopes: Optional[list[str]] = None,
        storage_dir: Optional[str] = None,
        token_file: Optional[str] = None,
    ) -> None:
        """
        Инициализировать CalendarAuth.

        Args:
            client_secrets_file: Путь к JSON-файлу с client secrets
                (скачанный из Google Cloud Console).
            encryption_key: Ключ для шифрования токенов. Если не задан —
                используется значение переменной окружения CALENDAR_ENCRYPTION_KEY.
            scopes: Список OAuth scopes. По умолчанию полный доступ к calendar + tasks.
            storage_dir: Директория для хранения зашифрованных токенов.
            token_file: Путь к файлу с зашифрованными credentials.

        Raises:
            AuthError: Если encryption_key не задан и переменная окружения не установлена.
        """
        self._client_secrets_file = client_secrets_file
        self._scopes = scopes or list(DEFAULT_SCOPES)
        self._token_file = token_file

        # Получаем encryption key
        key = encryption_key or os.environ.get("CALENDAR_ENCRYPTION_KEY")
        if not key:
            raise AuthError(
                "Encryption key обязателен. Задайте encryption_key параметр "
                "или CALENDAR_ENCRYPTION_KEY переменную окружения."
            )

        self._storage = SecureTokenStorage(
            encryption_key=key, storage_dir=storage_dir
        )
        self._credentials: Optional[Credentials] = None

        logger.info(
            "CalendarAuth инициализирован (scopes: %s)", self._scopes
        )

    # ------------------------------------------------------------------
    # Публичные методы
    # ------------------------------------------------------------------

    def authenticate(self) -> Credentials:
        """
        Получить валидные credentials, запустив OAuth flow при необходимости.

        Порядок действий:
            1. Проверяет наличие зашифрованных сохранённых credentials
            2. Если есть — загружает и проверяет валидность
            3. Если нет или невалидны — запускает OAuth flow
            4. Сохраняет новые credentials в зашифрованном виде

        Returns:
            Валидные Google OAuth2 Credentials.

        Raises:
            AuthError: Если аутентификация не удалась.
        """
        logger.info("Запуск аутентификации...")

        # Пробуем загрузить сохранённые credentials
        if self._storage.exists(self._token_file):
            try:
                self._credentials = self._storage.load(self._token_file)
                if self._credentials and self._credentials.valid:
                    logger.info("Загружены валидные сохранённые credentials")
                    return self._credentials
                logger.info("Сохранённые credentials невалидны, требуется обновление")
            except AuthError:
                logger.warning("Не удалось загрузить сохранённые credentials")

        # Если не удалось загрузить — запускаем OAuth flow
        return self._run_oauth_flow()

    def get_credentials(self) -> Credentials:
        """
        Получить текущие credentials (без запуска OAuth flow).

        Returns:
            Текущие Google OAuth2 Credentials.

        Raises:
            CredentialsNotFoundError: Если credentials не инициализированы.
        """
        if self._credentials and self._credentials.valid:
            return self._credentials

        # Пробуем загрузить из хранилища
        if self._storage.exists(self._token_file):
            self._credentials = self._storage.load(self._token_file)
            if self._credentials and self._credentials.valid:
                return self._credentials

        raise CredentialsNotFoundError(
            "Credentials не найдены. Вызовите authenticate() для авторизации."
        )

    def refresh_if_needed(self) -> bool:
        """
        Обновить access token если он истёк или скоро истечёт.

        Использует refresh token для получения нового access token.
        Обновлённые credentials автоматически сохраняются.

        Returns:
            True если токен был обновлён, False если он всё ещё валиден.

        Raises:
            TokenRefreshError: Если не удалось обновить токен
                (refresh token невалиден или отозван).
        """
        if not self._credentials:
            logger.warning("refresh_if_needed: credentials не инициализированы")
            return False

        # Если токен ещё валиден и не истекает в ближайшие 60 секунд
        if self._credentials.valid and not self._credentials.expired:
            return False

        if self._credentials.expired and self._credentials.refresh_token:
            logger.info("Access token истёк, выполняем refresh...")
            try:
                self._credentials.refresh(Request())
                # Сохраняем обновлённые credentials
                self._storage.store(self._credentials, self._token_file)
                logger.info("Токен успешно обновлён и сохранён")
                return True
            except HttpError as exc:
                status = exc.resp.status if hasattr(exc, "resp") else 0
                logger.error("Ошибка при refresh токена (HTTP %s): %s", status, exc)
                raise TokenRefreshError(
                    f"Не удалось обновить токен (HTTP {status}). "
                    "Возможно, refresh token отозван. Требуется повторная авторизация."
                ) from exc
            except Exception as exc:
                logger.error("Неожиданная ошибка при refresh токена: %s", exc)
                raise TokenRefreshError(f"Ошибка обновления токена: {exc}") from exc

        logger.warning("Невозможно обновить токен: нет refresh_token")
        raise TokenExpiredError(
            "Access token истёк и отсутствует refresh token. "
            "Требуется повторная авторизация через authenticate()."
        )

    def revoke(self) -> None:
        """
        Отозвать токены и удалить сохранённые credentials.

        После вызова требуется повторная авторизация.
        """
        if self._credentials and self._credentials.refresh_token:
            try:
                import requests
                requests.post(
                    "https://oauth2.googleapis.com/revoke",
                    params={"token": self._credentials.refresh_token},
                    timeout=10,
                )
                logger.info("Refresh token отозван на сервере Google")
            except Exception as exc:
                logger.warning("Не удалось отозвать токен на сервере: %s", exc)

        self._storage.delete(self._token_file)
        self._credentials = None
        logger.info("Credentials удалены из локального хранилища")

    def is_authenticated(self) -> bool:
        """Проверить, есть ли валидные credentials."""
        if self._credentials and self._credentials.valid:
            return True
        if self._storage.exists(self._token_file):
            try:
                self._credentials = self._storage.load(self._token_file)
                return self._credentials.valid
            except Exception:
                return False
        return False

    def build_service(self, api_name: str = "calendar", version: str = "v3") -> Resource:
        """
        Создать сервис Google API с текущими credentials.

        Args:
            api_name: Название API ('calendar' или 'tasks').
            version: Версия API.

        Returns:
            Экземпляр googleapiclient.discovery.Resource.

        Raises:
            CredentialsNotFoundError: Если credentials не инициализированы.
            AuthError: Если не удалось создать сервис.
        """
        creds = self.get_credentials()
        try:
            service = build(api_name, version, credentials=creds, cache_discovery=False)
            logger.debug("Создан сервис %s/%s", api_name, version)
            return service
        except Exception as exc:
            logger.error("Ошибка создания сервиса %s/%s: %s", api_name, version, exc)
            raise AuthError(f"Не удалось создать сервис {api_name}/{version}: {exc}") from exc

    # ------------------------------------------------------------------
    # Внутренние методы
    # ------------------------------------------------------------------

    def _run_oauth_flow(self) -> Credentials:
        """
        Запустить OAuth flow через локальный сервер.

        Открывает браузер пользователя для авторизации.
        Сохраняет полученные credentials в зашифрованном виде.

        Returns:
            Полученные Google OAuth2 Credentials.

        Raises:
            AuthError: Если OAuth flow не удалось выполнить.
            FileNotFoundError: Если файл client_secrets не найден.
        """
        if not os.path.exists(self._client_secrets_file):
            raise FileNotFoundError(
                f"Файл client secrets не найден: {self._client_secrets_file}. "
                f"Скачайте его из Google Cloud Console (Credentials > OAuth 2.0 Client IDs)."
            )

        logger.info("Запуск OAuth flow (браузер откроется автоматически)...")
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                self._client_secrets_file, self._scopes
            )
            # Настраиваем для получения refresh token
            flow.oauth2session.access_type = "offline"
            flow.oauth2session.prompt = "consent"  # Принудительно показываем consent screen

            self._credentials = flow.run_local_server(port=0)

            logger.info(
                "OAuth flow завершён успешно. Пользователь: %s",
                getattr(self._credentials, "client_id", "unknown"),
            )

            # Сохраняем в зашифрованном виде
            self._storage.store(self._credentials, self._token_file)

            return self._credentials

        except Exception as exc:
            logger.error("Ошибка OAuth flow: %s", exc)
            raise AuthError(f"OAuth flow не удался: {exc}") from exc


# ---------------------------------------------------------------------------
# Retry декоратор для API вызовов
# ---------------------------------------------------------------------------


def with_retry(
    max_retries: int = MAX_RETRIES,
    base_delay: float = BASE_RETRY_DELAY,
    max_delay: float = MAX_RETRY_DELAY,
    retryable_status_codes: Optional[set[int]] = None,
) -> Callable[[F], F]:
    """
    Декоратор: выполняет функцию с retry логикой и exponential backoff.

    При ошибках API (429, 500, 502, 503, 504) повторяет вызов
    с увеличивающейся задержкой (exponential backoff + jitter).

    Args:
        max_retries: Максимальное количество повторных попыток.
        base_delay: Базовая задержка в секундах.
        max_delay: Максимальная задержка в секундах.
        retryable_status_codes: Множество HTTP-кодов для retry.

    Returns:
        Декоратор, оборачивающий функцию retry-логикой.

    Example:
        >>> @with_retry(max_retries=3)
        ... def fetch_events():
        ...     return service.events().list(calendarId="primary").execute()
    """
    status_codes = retryable_status_codes or RETRYABLE_STATUS_CODES

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_error: Optional[Exception] = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except HttpError as exc:
                    status = exc.resp.status if hasattr(exc, "resp") else 0
                    last_error = exc

                    if status in status_codes:
                        # Exponential backoff с jitter
                        delay = min(
                            base_delay * (2 ** attempt) + random.uniform(0, 1),
                            max_delay,
                        )
                        logger.warning(
                            "API ошибка %s (попытка %d/%d), "
                            "повтор через %.1f сек...",
                            status, attempt + 1, max_retries, delay,
                        )

                        if status == 429:
                            # Rate limit — проверяем Retry-After header
                            retry_after = exc.resp.get("retry-after")
                            if retry_after:
                                delay = float(retry_after) + random.uniform(0, 1)
                                logger.info(
                                    "Получен Retry-After: %.1f сек", delay
                                )

                        time.sleep(delay)
                        continue

                    if status == 401:
                        logger.error("Ошибка авторизации (401): %s", exc)
                        raise TokenExpiredError(
                            "Токен истёк. Требуется обновление через refresh()."
                        ) from exc

                    if status == 403:
                        raise AuthError(
                            f"Доступ запрещён (403): {exc}", status_code=403
                        ) from exc

                    # Не retryable ошибка
                    raise

                except Exception as exc:
                    last_error = exc
                    logger.error(
                        "Неожиданная ошибка (попытка %d/%d): %s",
                        attempt + 1, max_retries, exc,
                    )
                    raise

            # Все попытки исчерпаны
            error_msg = str(last_error) if last_error else "Неизвестная ошибка"
            raise MaxRetriesExceededError(
                f"Функция {func.__name__} не выполнена",
                max_retries=max_retries,
                last_error=error_msg,
            )

        return wrapper  # type: ignore[return-value]
    return decorator


# Импорт base64 нужен для Fernet
import base64
