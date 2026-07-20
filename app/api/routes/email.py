from fastapi import APIRouter, Depends

from app.services.email import EmailService
from app.core.dependencies import get_email_service


router = APIRouter(
    prefix = "/api/email",
    tags = ["email"]
)

#Emailservice attualmente usa chiamate sincrone (TODO)
@router.post("/sync")
def sync(
    email_service: EmailService = Depends(get_email_service)
):
    result = email_service.sync()
    return {
        "fetched": result.fetched,
        "saved": result.saved,
        "skipped": result.skipped,
        "errors": result.errors
    }


@router.post("/initialize")
def initialize(
    email_service: EmailService = Depends(get_email_service)
):
    result = email_service.initialize()
    return {
        "fetched": result.fetched,
        "saved": result.saved,
        "skipped": result.skipped,
        "errors": result.errors
    }