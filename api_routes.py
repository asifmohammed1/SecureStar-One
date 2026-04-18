from fastapi import APIRouter
from llm_engine import call_llm

router = APIRouter(prefix="/v1", tags=["SecureStar API"])

@router.get("/status")
def get_status():
    """System health check."""
    return {"status": "operational", "security_level": "maximum"}

@router.post("/chat")
def security_chat(query: str):
    """Direct chat with the security specialist."""
    response = call_llm(query)
    return {"response": response}

@router.post("/auth/test-login")
def auth_vulnerability_test(user: str, passw: str):
    """Internal endpoint for BOLA and Broken Auth testing."""
    return {"message": "Endpoint monitored for scanning"}
