"""
AI reply endpoints for Smart HelpDesk.

These endpoints enqueue asynchronous tasks that generate AI‑powered
responses or summaries for a given ticket. They return a task identifier
that can be used to poll for the result. The actual computation is
performed in a Celery worker defined in ``app/workers/tasks.py``.
"""

from fastapi import APIRouter, HTTPException, status

from .tickets import TICKETS, Ticket
from ..workers.tasks import generate_reply_task, summarize_conversation_task  # type: ignore

router = APIRouter()


@router.post("/auto-reply/{ticket_id}")
async def auto_reply(ticket_id: str) -> dict[str, str]:
    """Queue a task to generate an AI reply for a ticket.

    Returns
    -------
    dict
        A response containing the Celery task ID.
    """
    if ticket_id not in TICKETS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    task = generate_reply_task.delay(ticket_id)
    return {"task_id": task.id}


@router.post("/summarize/{ticket_id}")
async def summarize(ticket_id: str) -> dict[str, str]:
    """Queue a task to summarize the conversation for a ticket."""
    if ticket_id not in TICKETS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    task = summarize_conversation_task.delay(ticket_id)
    return {"task_id": task.id}