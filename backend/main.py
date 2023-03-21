from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# TODO: Current implementation according to FastAPI docs
#  (https://fastapi.tiangolo.com/tutorial/security/get-current-user/#__tabbed_2_1)
def fake_decode_token(token):
    return schemas.User(
        rz_username=token + "fakedecoded", full_name="User", organisation_unit="1", has_admin_privileges=True
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """ Dependency, which returns the current user.
        - oauth2_scheme as sub-dependency
    :param token: str
    :return: current_user: User
    """
    user = fake_decode_token(token)
    return user


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/test/")
async def testing_auth(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@app.get("/users/me")
async def read_users_me(current_user: Annotated[schemas.User, Depends(get_current_user)]):
    return current_user
