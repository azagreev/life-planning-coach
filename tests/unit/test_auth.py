"""Unit tests for SecureTokenStorage and CalendarAuth in calendar_integration/auth.py."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from google.oauth2.credentials import Credentials

from calendar_integration.auth import CalendarAuth, SecureTokenStorage
from calendar_integration.exceptions import AuthError, CredentialsNotFoundError


class FakeCredentials:
    """A picklable stand-in for google.oauth2.credentials.Credentials."""

    def __init__(self, valid: bool = True, expired: bool = False):
        self.valid = valid
        self.expired = expired
        self.refresh_token = "fake-refresh-token"
        self.token = "fake-token"

    def to_json(self) -> str:
        return json.dumps({
            "token": self.token,
            "refresh_token": self.refresh_token,
            "client_id": "fake-client-id",
            "client_secret": "fake-client-secret",
            "token_uri": "https://oauth2.googleapis.com/token",
            "type": "authorized_user",
            "expiry": "2099-01-01T00:00:00Z",
        })


class TestSecureTokenStorage(unittest.TestCase):
    """Tests for SecureTokenStorage."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage_dir = self.temp_dir.name
        self.key = "a-very-strong-password-12345"
        self.storage = SecureTokenStorage(encryption_key=self.key, storage_dir=self.storage_dir)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _make_credentials(self) -> Credentials:
        """Build a minimal Credentials instance for testing."""
        return Credentials(
            token="fake-access-token",
            refresh_token="fake-refresh-token",
            token_uri="https://oauth2.googleapis.com/token",
            client_id="fake-client-id",
            client_secret="fake-client-secret",
            scopes=["https://www.googleapis.com/auth/calendar"],
        )

    def test_store_and_load_with_valid_key(self) -> None:
        """store() encrypts and load() decrypts successfully with the correct key."""
        creds = self._make_credentials()
        path = self.storage.store(creds)

        assert self.storage.exists(path)
        loaded = self.storage.load(path)
        assert isinstance(loaded, Credentials)
        assert loaded.token == creds.token
        assert loaded.refresh_token == creds.refresh_token

    def test_load_with_wrong_key_raises_auth_error(self) -> None:
        """Loading with a different encryption key must raise AuthError."""
        creds = self._make_credentials()
        path = self.storage.store(creds)

        wrong_storage = SecureTokenStorage(
            encryption_key="totally-different-password",
            storage_dir=self.storage_dir,
        )
        with pytest.raises(AuthError):
            wrong_storage.load(path)

    def test_exists_returns_true_after_store(self) -> None:
        """exists() should return True after store() and False after delete()."""
        creds = self._make_credentials()
        path = self.storage.store(creds)

        assert self.storage.exists(path) is True
        self.storage.delete(path)
        assert self.storage.exists(path) is False

    def test_key_too_short_raises_error(self) -> None:
        """A key shorter than some minimum length should raise an error.

        NOTE: This test is written in anticipation of key-length validation.
        It will fail until the validation is implemented in SecureTokenStorage.
        """
        with pytest.raises(AuthError):
            SecureTokenStorage(encryption_key="short", storage_dir=self.storage_dir)

    def test_load_nonexistent_file_raises_credentials_not_found(self) -> None:
        """Loading a missing file must raise CredentialsNotFoundError."""
        missing = Path(self.storage_dir) / "nonexistent.enc"
        with pytest.raises(CredentialsNotFoundError):
            self.storage.load(str(missing))


class TestCalendarAuth(unittest.TestCase):
    """Tests for CalendarAuth."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage_dir = self.temp_dir.name
        self.key = "my-test-encryption-key-123456"
        self.auth = CalendarAuth(
            client_secrets_file="dummy_credentials.json",
            encryption_key=self.key,
            storage_dir=self.storage_dir,
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _make_credentials(self, valid: bool = True, expired: bool = False) -> FakeCredentials:
        """Return a picklable fake Credentials object."""
        return FakeCredentials(valid=valid, expired=expired)

    def test_init_without_key_raises_auth_error(self) -> None:
        """CalendarAuth must raise AuthError when no encryption key is provided."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(AuthError):
                CalendarAuth(client_secrets_file="dummy.json")

    def test_init_uses_env_var(self) -> None:
        """CalendarAuth should fall back to CALENDAR_ENCRYPTION_KEY env var."""
        with patch.dict(os.environ, {"CALENDAR_ENCRYPTION_KEY": self.key}):
            auth = CalendarAuth(
                client_secrets_file="dummy.json",
                storage_dir=self.storage_dir,
            )
        assert auth is not None

    def test_authenticate_loads_valid_stored_credentials(self) -> None:
        """authenticate() loads existing credentials when they are valid."""
        creds = self._make_credentials(valid=True, expired=False)
        self.auth._storage.store(creds, self.auth._token_file)

        result = self.auth.authenticate()
        # pickle.loads creates a new object, so check attributes instead of identity
        assert result.valid is True
        assert result.token == creds.token
        assert result.refresh_token == creds.refresh_token

    def test_authenticate_runs_oauth_when_no_stored_credentials(self) -> None:
        """authenticate() runs OAuth flow when nothing is stored."""
        mock_creds = self._make_credentials(valid=True)
        with patch.object(
            self.auth, "_run_oauth_flow", return_value=mock_creds
        ) as mock_oauth:
            result = self.auth.authenticate()
            mock_oauth.assert_called_once()
            assert result is mock_creds

    def test_get_credentials_returns_valid_credentials(self) -> None:
        """get_credentials() returns credentials when they are valid."""
        creds = self._make_credentials(valid=True)
        self.auth._credentials = creds
        assert self.auth.get_credentials() is creds

    def test_get_credentials_raises_when_none(self) -> None:
        """get_credentials() raises CredentialsNotFoundError when no valid creds exist."""
        self.auth._credentials = None
        with pytest.raises(CredentialsNotFoundError):
            self.auth.get_credentials()

    def test_is_authenticated_true_when_valid(self) -> None:
        """is_authenticated() returns True for valid in-memory credentials."""
        creds = self._make_credentials(valid=True)
        self.auth._credentials = creds
        assert self.auth.is_authenticated() is True

    def test_is_authenticated_false_when_invalid(self) -> None:
        """is_authenticated() returns False when credentials are invalid."""
        self.auth._credentials = None
        assert self.auth.is_authenticated() is False

    def test_revoke_deletes_storage_and_clears_creds(self) -> None:
        """revoke() deletes stored file and clears in-memory credentials."""
        creds = self._make_credentials(valid=True)
        self.auth._credentials = creds
        self.auth._storage.store(creds, self.auth._token_file)

        with patch("requests.post"):
            self.auth.revoke()

        assert self.auth._credentials is None
        assert self.auth._storage.exists(self.auth._token_file) is False
