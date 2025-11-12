"""
Entry point for the FastAPI application used in the Smart HelpDesk backend.

This module defines a minimal FastAPI app that mounts the various API routes
used by the help‑desk system. It is intentionally lightweight; most of the
business logic lives in the individual route modules found in
``app/api/routes``. The purpose of this file is to assemble all of those
routes together and provide a single ASGI application instance for Uvicorn
to run.

To run this application locally you can execute the following command
from the ``backend`` directory:

    uvicorn app.main:app --reload

The ``--reload`` flag will automatically restart the server whenever you
change Python files.
"""

from fastapi import FastAPI

from .api import routes as api_routes

# Create the FastAPI application instance.
app = FastAPI(title="Smart HelpDesk API")

# Include all API routers from the routes package. Each router defines
# its own prefix (e.g. /auth, /tickets) so including the router here
# automatically registers its endpoints.
app.include_router(api_routes.router)


@app.get("/health", tags=["health"])
async def healthcheck() -> dict[str, str]:
    """Simple healthcheck endpoint to verify the service is running.

    Returns
    -------
    dict[str, str]
        A message indicating the service is up.
    """
    return {"status": "ok"}