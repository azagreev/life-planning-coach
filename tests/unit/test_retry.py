"""Unit tests for the with_retry decorator in calendar_integration/auth.py."""

import unittest
from http.client import HTTPResponse
from io import BytesIO
from unittest.mock import MagicMock, patch

import pytest

from calendar_integration.auth import with_retry
from calendar_integration.exceptions import (
    AuthError,
    MaxRetriesExceededError,
    TokenExpiredError,
)


def _make_http_error(status: int, retry_after: str | None = None) -> Exception:
    """Create a mock googleapiclient.errors.HttpError with the given status code.

    The real HttpError constructor requires an httplib2 response object and bytes
    content.  We patch the class so that a simple MagicMock is accepted.
    """
    from googleapiclient.errors import HttpError

    resp = MagicMock()
    resp.status = status
    resp.get = MagicMock(return_value=retry_after)
    # HttpError expects (resp, content) but we can create it manually via __new__
    # or just instantiate and set attributes after suppressing __init__.
    exc = HttpError.__new__(HttpError)
    exc.resp = resp
    exc._exc = None
    exc.error_details = None
    exc.uri = "http://example.com"
    exc.reason = f"Mock HTTP {status}"
    return exc


class TestWithRetry(unittest.TestCase):
    """Tests for the with_retry decorator."""

    def test_retry_on_429_rate_limit(self) -> None:
        """429 triggers retry and eventually succeeds."""
        mock_func = MagicMock(side_effect=[
            _make_http_error(429),
            _make_http_error(429),
            "success",
        ])
        decorated = with_retry(max_retries=3, base_delay=0.1)(mock_func)

        with patch("calendar_integration.auth.time.sleep"):
            result = decorated()

        assert result == "success"
        assert mock_func.call_count == 3

    def test_retry_on_500_502_503_504(self) -> None:
        """500, 502, 503, 504 all trigger retry logic."""
        for status in (500, 502, 503, 504):
            mock_func = MagicMock(side_effect=[
                _make_http_error(status),
                "ok",
            ])
            decorated = with_retry(max_retries=2, base_delay=0.01)(mock_func)

            with patch("calendar_integration.auth.time.sleep"):
                result = decorated()

            assert result == "ok"
            assert mock_func.call_count == 2

    def test_401_raises_token_expired_immediately(self) -> None:
        """401 without auth_instance must raise TokenExpiredError without retrying."""
        mock_func = MagicMock(side_effect=[_make_http_error(401)])
        decorated = with_retry(max_retries=3, base_delay=0.01)(mock_func)

        with pytest.raises(TokenExpiredError):
            decorated()

        mock_func.assert_called_once()

    def test_401_with_auth_instance_refreshes_and_retries(self) -> None:
        """401 with auth_instance triggers refresh and retries once."""
        mock_auth = MagicMock()
        mock_func = MagicMock(side_effect=[_make_http_error(401), "success"])
        decorated = with_retry(
            max_retries=3, base_delay=0.01, auth_instance=mock_auth
        )(mock_func)

        with patch("calendar_integration.auth.time.sleep"):
            result = decorated()

        assert result == "success"
        assert mock_func.call_count == 2
        mock_auth.refresh_if_needed.assert_called_once()

    def test_401_with_auth_instance_fails_after_refresh(self) -> None:
        """If 401 persists after refresh, raise TokenExpiredError."""
        mock_auth = MagicMock()
        mock_func = MagicMock(
            side_effect=[_make_http_error(401), _make_http_error(401)]
        )
        decorated = with_retry(
            max_retries=3, base_delay=0.01, auth_instance=mock_auth
        )(mock_func)

        with patch("calendar_integration.auth.time.sleep"):
            with pytest.raises(TokenExpiredError):
                decorated()

        assert mock_func.call_count == 2
        mock_auth.refresh_if_needed.assert_called_once()

    def test_exponential_backoff_timing(self) -> None:
        """Exponential backoff delays should follow base_delay * 2^attempt + jitter."""
        mock_func = MagicMock(side_effect=[
            _make_http_error(500),
            _make_http_error(500),
            _make_http_error(500),
        ])
        mock_func.__name__ = "mock_func"
        decorated = with_retry(max_retries=3, base_delay=1.0, max_delay=100.0)(mock_func)

        sleeps = []

        def capture_sleep(seconds: float) -> None:
            sleeps.append(seconds)

        with patch("calendar_integration.auth.time.sleep", side_effect=capture_sleep):
            with patch("calendar_integration.auth.random.uniform", return_value=0.5):
                with pytest.raises(MaxRetriesExceededError):
                    decorated()

        # attempt=0 -> 1.0 * 1 + 0.5 = 1.5
        # attempt=1 -> 1.0 * 2 + 0.5 = 2.5
        # attempt=2 -> 1.0 * 4 + 0.5 = 4.5
        assert sleeps == [1.5, 2.5, 4.5]

    def test_429_uses_retry_after_header(self) -> None:
        """When 429 includes Retry-After header, the delay uses that value."""
        mock_func = MagicMock(side_effect=[
            _make_http_error(429, retry_after="10"),
            "success",
        ])
        decorated = with_retry(max_retries=2, base_delay=1.0)(mock_func)

        sleeps = []

        def capture_sleep(seconds: float) -> None:
            sleeps.append(seconds)

        with patch("calendar_integration.auth.time.sleep", side_effect=capture_sleep):
            with patch("calendar_integration.auth.random.uniform", return_value=0.25):
                result = decorated()

        assert result == "success"
        # delay = float("10") + 0.25 = 10.25
        assert sleeps == [10.25]

    def test_max_retries_exceeded_error(self) -> None:
        """After all retries are exhausted MaxRetriesExceededError is raised."""
        mock_func = MagicMock(side_effect=[_make_http_error(503)] * 3)
        mock_func.__name__ = "mock_func"
        decorated = with_retry(max_retries=3, base_delay=0.01)(mock_func)

        with patch("calendar_integration.auth.time.sleep"):
            with pytest.raises(MaxRetriesExceededError) as exc_info:
                decorated()

        assert mock_func.call_count == 3
        assert exc_info.value.max_retries == 3
        assert "503" in str(exc_info.value.last_error)

    def test_non_retryable_error_raises_immediately(self) -> None:
        """404 (not in retryable status codes) must raise immediately."""
        mock_func = MagicMock(side_effect=[_make_http_error(404)])
        decorated = with_retry(max_retries=3, base_delay=0.01)(mock_func)

        with pytest.raises(Exception) as exc_info:
            decorated()

        mock_func.assert_called_once()
        # Verify it is the original HttpError, not wrapped
        assert hasattr(exc_info.value, "resp")
        assert exc_info.value.resp.status == 404

    def test_403_raises_auth_error(self) -> None:
        """403 must raise AuthError without retrying."""
        mock_func = MagicMock(side_effect=[_make_http_error(403)])
        decorated = with_retry(max_retries=3, base_delay=0.01)(mock_func)

        with pytest.raises(AuthError) as exc_info:
            decorated()

        mock_func.assert_called_once()
        assert exc_info.value.status_code == 403
