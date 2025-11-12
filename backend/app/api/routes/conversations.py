"""
Conversation endpoints for Smart HelpDesk.

Each ticket can have a list of messages exchanged between the customer
and the support agent. This module defines endpoints to list messages
for a ticket and add new messages. The messages are stored in a
process‑local structure for demonstration purposes.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List

from fastapi import APIRouter, HTTPException, status

from .tickets import TICKETS


@dataclass
class Message:
    """Represents a single chat message in a conversation."""
    role: str
    content: str
    timestamp: str = datetime.utcnow().isoformat()


# In‑memory store of messages per ticket ID.
CONVERSATIONS: Dict[str, List[Message]] = {}

router = APIRouter()


@router.get("/{ticket_id}")
async def list_messages(ticket_id: str) -> List[Dict[str, str]]:
    """Return the messages for a given ticket."""
    if ticket_id not in TICKETS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return [asdict(msg) for msg in CONVERSATIONS.get(ticket_id, [])]


@router.post("/{ticket_id}")
async def add_message(ticket_id: str, role: str, content: str) -> Dict[str, str]:
    """Add a message to the conversation for a ticket."""
    if ticket_id not in TICKETS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    message = Message(role=role, content=content)
    CONVERSATIONS.setdefault(ticket_id, []).append(message)
    return asdict(message)