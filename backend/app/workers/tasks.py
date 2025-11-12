"""
Background tasks for Smart HelpDesk.

This module defines Celery tasks that perform long‑running or blocking
operations. In particular, we generate AI replies using OpenAI's
ChatCompletion API and summarise entire ticket conversations. Moving
these operations into background tasks allows the FastAPI request
handlers to return immediately and keeps the service responsive.

The functions defined here are intentionally simple and include
placeholder error handling. You can extend these implementations to
handle retries, logging and fine‑tune the prompts for better results.
"""

import os
from typing import List

from openai import OpenAI

from .celery_app import celery_app
from ..api.routes.conversations import CONVERSATIONS


# OpenAI API key must be provided via environment variable. When running
# locally you can export OPENAI_API_KEY before starting the worker.
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Initialise the OpenAI client lazily. If the API key is not set the
# client will throw during calls – in that case tasks will return a
# generic error message.
_openai_client = None


def get_openai_client() -> OpenAI:
    """Get or create a singleton OpenAI client."""
    global _openai_client
    if _openai_client is None:
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is not configured for OpenAI tasks")
        _openai_client = OpenAI(api_key=OPENAI_API_KEY)
    return _openai_client


def _conversation_to_prompt(messages: List[dict[str, str]]) -> str:
    """Convert a conversation into a prompt for the LLM.

    This helper function flattens the message list into a single prompt
    string. You can customise this to provide context for your model.
    """
    parts = []
    for msg in messages:
        parts.append(f"{msg['role']}: {msg['content']}")
    return "\n".join(parts)


@celery_app.task(name="generate_reply_task")
def generate_reply_task(ticket_id: str) -> str:
    """Generate an AI reply based on the conversation for a ticket."""
    messages = [msg for msg in CONVERSATIONS.get(ticket_id, [])]
    if not messages:
        return "No conversation found to generate a reply."
    prompt = _conversation_to_prompt([m.__dict__ for m in messages])
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # use a small model to reduce cost
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        reply = response.choices[0].message.content.strip()
    except Exception as exc:
        # In case of failure return a generic message. In production you
        # should log the exception details for later inspection.
        reply = f"[Error generating reply: {exc}]"
    return reply


@celery_app.task(name="summarize_conversation_task")
def summarize_conversation_task(ticket_id: str) -> str:
    """Summarize the conversation for a ticket."""
    messages = [msg for msg in CONVERSATIONS.get(ticket_id, [])]
    if not messages:
        return "No conversation found to summarize."
    prompt = _conversation_to_prompt([m.__dict__ for m in messages])
    prompt = f"Please provide a concise summary of the following conversation:\n\n{prompt}"
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        summary = response.choices[0].message.content.strip()
    except Exception as exc:
        summary = f"[Error summarizing conversation: {exc}]"
    return summary