"""
Celery application setup for Smart HelpDesk.

This module defines the Celery application used to run background tasks
such as generating AI replies and summarizing conversations. It must be
imported by any module that defines tasks. Configuration is read from
environment variables or uses reasonable defaults for local development.
"""

import os

from celery import Celery


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "smart_helpdesk",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

# Celery configuration options can be set here. For this example we leave
# most settings at their defaults. In production you should configure
# serialization, time limits and other options as needed.
