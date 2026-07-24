import os

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers.audit import router as audit_router


app = FastAPI(title="Page Pulse API")

allowed_origins = os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def handle_request_validation_error(
    _request: Request, _exc: RequestValidationError
) -> JSONResponse:
    """Return a consistent client error for invalid audit requests."""
    return JSONResponse(
        status_code=400,
        content={"detail": "A valid HTTP or HTTPS URL is required."},
    )


app.include_router(audit_router, prefix="/api")
