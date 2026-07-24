from pydantic import BaseModel, HttpUrl


class AuditRequest(BaseModel):
    url: HttpUrl


class AuditResponse(BaseModel):
    url: str
    status_code: int
    response_time_ms: int
    title: str | None
    meta_description: str | None
    h1_count: int
    images_missing_alt: int
    word_count: int
