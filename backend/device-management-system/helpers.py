import uuid

from fastapi import HTTPException, status

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Die Login-Daten konnten nicht überprüft werden.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_uuid() -> str:
    return str(uuid.uuid4())
