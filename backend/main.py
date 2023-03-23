from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
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
        "organisation_unit": "Medieninformatik",
        "has_admin_privileges": False,
        "hashed_password": "fakehashed1234"
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
        return schemas.UserCreate(**user_dict)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """ Dependency, which returns the current user.
        - oauth2_scheme as sub-dependency
    :param token: str
    :return: current_user: User
    """
    user = fake_decode_token(token)
    # Exception code taken from https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    """
    Login-Route, which receives form data containing username and password as well as the scope of the login (optional)
    :param form_data:
    :return:
    TODO: Current implementation taken from https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
    """
    user_from_db = crud.get_user_by_username(db, form_data.username)
    if not user_from_db:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user_from_db.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user_from_db.rz_username, "token_type": "bearer"}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/test/")
async def testing_auth(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@app.get("/users/me")
async def read_users_me(current_user: Annotated[schemas.User, Depends(get_current_user)]):
    return current_user
