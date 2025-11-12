"""
Authentication endpoints for the Smart HelpDesk system.

At this stage the authentication endpoints are intentionally simplified.
They provide placeholder behaviour that can be expanded later to integrate
with a proper user database and password hashing. The ``login`` endpoint
issues a dummy JSON Web Token (JWT) and the ``register`` endpoint simply
acknowledges receipt of a new user. These endpoints demonstrate how
dependency injection and response models could be structured without
introducing heavy‑weight authentication logic into this example.
"""

from datetime import datetime, timedelta
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, status

import jose.jwt as jwt


SECRET_KEY = "dummy_secret_key_change_me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()


def create_access_token(data: Dict[str, Any], expires_delta: timedelta) -> str:
    """Generate a signed JSON Web Token.

    Parameters
    ----------
    data : dict
        Payload to encode in the token.
    expires_delta : timedelta
        Expiration time for the token.

    Returns
    -------
    str
        Encoded JWT.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # type: ignore
    return encoded_jwt


@router.post("/login")
async def login(username: str, password: str) -> Dict[str, str]:
    """Authenticate a user and return a bearer token.

    This dummy implementation accepts any username/password combination
    and returns a signed JWT. In a real application you should verify
    the provided credentials against a user database and hash passwords
    rather than storing them in plain text.
    """
    # In a real implementation you would verify the user exists and
    # check the password here. We skip that for brevity.
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
async def register(username: str, password: str) -> Dict[str, str]:
    """Register a new user.

    Acknowledge the registration request. In a real implementation you
    would write the new user to a database and hash their password.
    """
    # Placeholder for user creation logic.
    # For now simply return a success message.
    return {"message": f"User {username} registered successfully"}