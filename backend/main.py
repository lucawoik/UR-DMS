from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import variables
from . import crud, models, schemas
from .database import SessionLocal, engine


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# TODO: Remove
def fake_hash_password(password: str):
    return "fakehashed" + password


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
                                  hashed_password=get_password_hash(variables.USER_PASSWORD))
        crud.create_user(db, user)
    else:
        print("User with rz_username: user exists already")
    # Checking for existing user with username "admin" and creating a new one if not existent
    if not crud.get_user_by_username(db, "admin"):
        admin = schemas.UserCreate(rz_username="admin",
                                   full_name="User Admin",
                                   organisation_unit="2222222",
                                   has_admin_privileges=True,
                                   hashed_password=get_password_hash(variables.ADMIN_PASSWORD))
        crud.create_user(db, admin)
    else:
        print("User with rz_username: admin exists already")


# Calling prepare_db() method
prepare_db()


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


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Function which creates an access token to be handed out after successful login
    :param data:
    :param expires_delta:
    :return:
    TODO: Code taken from https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, variables.SECRET_KEY, algorithm=variables.ALGORITHM)
    return encoded_jwt


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    """
    Login-Route, which receives form data containing username and password as well as the scope of the login (optional)
    :param db:
    :param form_data:
    :return:
    TODO: Current implementation taken from https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=variables.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.rz_username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=schemas.User)
async def read_users_me(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    """
    Returns the currently authenticated user using the token given from oauth2
    :param token:
    :param db:
    :return:
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, variables.SECRET_KEY, algorithms=[variables.ALGORITHM])
        rz_username: str = payload.get("sub")
        if rz_username is None:
            raise credentials_exception
        token_data = schemas.TokenData(rz_username=rz_username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, rz_username=token_data.rz_username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/import")
async def import_database_json(file: UploadFile):
    """
    Takes a .json file and imports it onto the existing database.
        - Existing entries in the database are not deleted
        - Merge conflicts are ignored
    :return:
    """
    return {"filename": file.filename}


@app.get("/export")
async def export_database_json():
    """
    Exports the entire database as .json file aside from the 'users' table.
    :return:
    """
    return None


@app.delete("/purge")
async def purge_database():
    """
    Purges the entire database aside from the 'users' table
    :return:
    """
    return None


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
