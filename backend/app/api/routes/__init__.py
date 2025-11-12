"""
API routing package.

This package groups all of the FastAPI routers that make up the public
interface for the Smart HelpDesk backend. Each module defines a router
handling a specific domain (authentication, tickets, conversations and
AI‑powered replies). The routers are combined in this package so that the
main application can include them all at once.
"""

from fastapi import APIRouter

from .auth import router as auth_router
from .tickets import router as tickets_router
from .conversations import router as conversations_router
from .gpt_reply import router as gpt_router

# Top‑level API router combining all sub‑routers. When included in
# ``app.main.app`` this will expose endpoints like ``/auth/login`` or
# ``/tickets/{ticket_id}``.
router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(tickets_router, prefix="/tickets", tags=["tickets"])
router.include_router(conversations_router, prefix="/conversations", tags=["conversations"])
router.include_router(gpt_router, prefix="/gpt", tags=["ai"])