from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import variables
from . import crud, models, schemas
from .database import SessionLocal, engine


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


def verify_password(plain_password, hashed_password):
    """
    Method to verify the given password in plain text against the hashed string
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Generating the hash from the password in plain text
    :param password:
    :return:
    """
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str):
    """
    Authenticating the user by getting the user from the db and verifying the password.
    :param db:
    :param username:
    :param password:
    :return:
    """
    user = crud.get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# TODO: Remove print statements
def prepare_db():
    """
    Method which prepares the database with the necessary user data.
    :return:
    """
    db = SessionLocal()
    # Checking for existing user with username "user" and creating a new one if not existent
    if not crud.get_user_by_username(db, "user"):
        user = schemas.UserCreate(rz_username="user",
                                  full_name="User User",
                                  organisation_unit="1111111",
                                  has_admin_privileges=False,
                                  hashed_password=fake_hash_password("1234"))
        crud.create_user(db, user)
    else:
        print("User with rz_username: user exists already")
    # Checking for existing user with username "admin" and creating a new one if not existent
    if not crud.get_user_by_username(db, "admin"):
        admin = schemas.UserCreate(rz_username="admin",
                                   full_name="User Admin",
                                   organisation_unit="2222222",
                                   has_admin_privileges=True,
                                   hashed_password=fake_hash_password("vollgeheim"))
        crud.create_user(db, admin)
    else:
        print("User with rz_username: admin exists already")


# Calling prepare_db() method
prepare_db()


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    """
    Login-Route, which receives form data containing username and password as well as the scope of the login (optional)
    :param db:
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


@app.get("/users/me", response_model=schemas.User)
async def read_users_me(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    """
    Returns the currently authenticated user using the token given from oauth2
    :param token:
    :param db:
    :return:
    """
    current_user = crud.get_user_by_username(db, token)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/test/")
async def testing_auth(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@app.get("/users/")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/by-username/{username}/", response_model=schemas.User)
def read_users_by_username(rz_username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, rz_username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
