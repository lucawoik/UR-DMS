from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# TODO: For now using a fake-db (dictionary), needs to be replaced with backend.db later
fake_users_db = {
    "user": {
        "rz_username": "user",
        "full_name": "Max Mustermann",
        "organisation_unit" : "Medieninformatik",
        "has_admin_privileges": False,
        "hashed_password": "1234"
    }
}


# TODO: Current implementation according to FastAPI docs
#  (https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/)
def fake_decode_token(token):
    """ This method decodes the token that is given from the authentication process and gets the corresponding
    user from the database.
    :param token:
    :return:
    """
    user = get_user(fake_users_db, token)
    return user


def get_user(db, rz_username: str):
    """ Helper function which gets the user from the fake-db dictionary
    :param db:
    :param rz_username:
    :return:
    """
    if rz_username in db:
        user_dict = db[rz_username]
        return schemas.UserInDB(**user_dict)


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
