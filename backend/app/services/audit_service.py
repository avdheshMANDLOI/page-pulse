import time

import httpx
from bs4 import BeautifulSoup
from fastapi import HTTPException, status

from app.schemas.audit import AuditResponse


REQUEST_TIMEOUT_SECONDS = 10.0


async def audit_webpage(url: str) -> AuditResponse:
    """Retrieve an HTML page and calculate its audit values."""
    try:
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=httpx.Timeout(REQUEST_TIMEOUT_SECONDS),
            headers={"User-Agent": "PagePulse/1.0"},
        ) as client:
            started_at = time.perf_counter()
            response = await client.get(url)
            response_time_ms = round((time.perf_counter() - started_at) * 1000)
    except httpx.TimeoutException as exc:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="The webpage did not respond within 10 seconds.",
        ) from exc
    except httpx.ConnectError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not connect to the webpage. Check the URL and try again.",
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The webpage could not be fetched.",
        ) from exc

    if not _is_html_response(response):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="The provided URL does not point to an HTML page.",
        )

    try:
        return _build_audit_response(response, response_time_ms)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The webpage could not be analysed.",
        ) from exc


def _is_html_response(response: httpx.Response) -> bool:
    content_type = response.headers.get("content-type", "")
    return "text/html" in content_type.lower()


def _build_audit_response(response: httpx.Response, response_time_ms: int) -> AuditResponse:
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else None
    description_tag = soup.find("meta", attrs={"name": "description"})
    meta_description = (
        description_tag.get("content", "").strip() if description_tag else None
    )

    for element in soup(["script", "style", "noscript"]):
        element.decompose()

    word_count = len(soup.get_text(" ", strip=True).split())
    images_missing_alt = sum(
        not image.get("alt", "").strip() for image in soup.find_all("img")
    )

    return AuditResponse(
        url=str(response.url),
        status_code=response.status_code,
        response_time_ms=response_time_ms,
        title=title,
        meta_description=meta_description,
        h1_count=len(soup.find_all("h1")),
        images_missing_alt=images_missing_alt,
        word_count=word_count,
    )
