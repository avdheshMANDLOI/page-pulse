from fastapi import APIRouter

from app.schemas.audit import AuditRequest, AuditResponse
from app.services.audit_service import audit_webpage


router = APIRouter(tags=["audit"])


@router.post("/audit", response_model=AuditResponse)
async def audit(request: AuditRequest) -> AuditResponse:
    """Fetch and analyse a webpage."""
    return await audit_webpage(str(request.url))
