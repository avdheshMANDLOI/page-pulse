import asyncio
from collections.abc import Callable
from typing import TypeAlias
from unittest.mock import patch

import httpx
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.main import app
from app.services.audit_service import audit_webpage


MockResult: TypeAlias = httpx.Response | Exception


class AsyncClientStub:
    """Async client replacement that returns a fixed result without network access."""

    def __init__(self, result: MockResult) -> None:
        self.result = result

    async def __aenter__(self) -> "AsyncClientStub":
        return self

    async def __aexit__(self, *_args: object) -> None:
        return None

    async def get(self, _url: str) -> httpx.Response:
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


@pytest.fixture
def make_response() -> Callable[[str, str], httpx.Response]:
    def _make_response(content_type: str, html: str = "") -> httpx.Response:
        return httpx.Response(
            200,
            headers={"content-type": content_type},
            content=html.encode(),
            request=httpx.Request("GET", "https://example.com"),
        )

    return _make_response


def test_audit_webpage_extracts_metrics_from_html(
    make_response: Callable[[str, str], httpx.Response],
) -> None:
    html = """
    <html>
      <head>
        <title>Example article</title>
        <meta name="description" content="A short page description.">
      </head>
      <body>
        <h1>First heading</h1>
        <h1>Second heading</h1>
        <p>One two three four five.</p>
        <img src="missing-alt.png">
        <img src="empty-alt.png" alt="">
        <img src="described.png" alt="Described image">
        <script>this text must not count</script>
      </body>
    </html>
    """
    response = make_response("text/html; charset=utf-8", html)

    with patch(
        "app.services.audit_service.httpx.AsyncClient",
        return_value=AsyncClientStub(response),
    ):
        result = asyncio.run(audit_webpage("https://example.com"))

    assert result.title == "Example article"
    assert result.meta_description == "A short page description."
    assert result.h1_count == 2
    assert result.images_missing_alt == 2
    assert result.word_count == 11


def test_api_returns_bad_request_for_invalid_url() -> None:
    response = TestClient(app).post("/api/audit", json={"url": "not-a-url"})

    assert response.status_code == 400
    assert response.json() == {"detail": "A valid HTTP or HTTPS URL is required."}


def test_audit_webpage_rejects_non_html_response(
    make_response: Callable[[str, str], httpx.Response],
) -> None:
    response = make_response("application/pdf")

    with patch(
        "app.services.audit_service.httpx.AsyncClient",
        return_value=AsyncClientStub(response),
    ):
        with pytest.raises(HTTPException) as exception_info:
            asyncio.run(audit_webpage("https://example.com/report.pdf"))

    assert exception_info.value.status_code == 415
    assert exception_info.value.detail == "The provided URL does not point to an HTML page."


def test_audit_webpage_returns_request_timeout_when_fetch_times_out() -> None:
    timeout = httpx.ReadTimeout("Request timed out")

    with patch(
        "app.services.audit_service.httpx.AsyncClient",
        return_value=AsyncClientStub(timeout),
    ):
        with pytest.raises(HTTPException) as exception_info:
            asyncio.run(audit_webpage("https://example.com"))

    assert exception_info.value.status_code == 408
    assert exception_info.value.detail == "The webpage did not respond within 10 seconds."
