"""
Ticket management endpoints for Smart HelpDesk.

These endpoints demonstrate basic CRUD (create, read, update) operations
for help‑desk tickets. For simplicity the tickets are stored in a
process‑local dictionary rather than a persistent database. The schema
can easily be swapped out for SQLAlchemy models backed by a real
database if needed.
"""

import uuid
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException, status


@dataclass
class Ticket:
    """Data structure representing a support ticket."""

    title: str
    description: str
    status: str = "open"
    assignee: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


# In‑memory store for tickets. In production use a database.
TICKETS: Dict[str, Ticket] = {}

router = APIRouter()


@router.get("/")
async def list_tickets() -> List[Dict[str, str]]:
    """Return a list of all tickets."""
    return [asdict(ticket) for ticket in TICKETS.values()]


@router.post("/")
async def create_ticket(title: str, description: str) -> Dict[str, str]:
    """Create a new ticket."""
    ticket = Ticket(title=title, description=description)
    TICKETS[ticket.id] = ticket
    return asdict(ticket)


@router.get("/{ticket_id}")
async def get_ticket(ticket_id: str) -> Dict[str, str]:
    """Retrieve a ticket by ID."""
    ticket = TICKETS.get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return asdict(ticket)


@router.patch("/{ticket_id}")
async def update_ticket(ticket_id: str, status: Optional[str] = None, assignee: Optional[str] = None) -> Dict[str, str]:
    """Update a ticket's status or assignee."""
    ticket = TICKETS.get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    if status is not None:
        ticket.status = status
    if assignee is not None:
        ticket.assignee = assignee
    return asdict(ticket)