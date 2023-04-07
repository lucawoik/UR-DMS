import json
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
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


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


@app.post("/token", tags=["Authentication"])
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


@app.get("/users/me", response_model=schemas.User, tags=["Authentication"])
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


@app.post("/import", tags=["Import/Export/Purge Database"])
async def import_database_json(file: UploadFile, db: Session = Depends(get_db)):
    """
    Takes a .json file and imports it onto the existing database.
        - Existing entries in the database are not deleted
        - Merge conflicts are ignored
    :return:
    """
    data = json.loads(await file.read())
    success = crud.import_json(db, data)
    if success:
        return {"filename": file.filename}
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unique constraint was violated by the imported data."
        )


@app.get("/export", tags=["Import/Export/Purge Database"])
async def export_database_json(db: Session = Depends(get_db)):
    """
    Exports the entire database as .json file aside from the 'users' table.
    :return:
    """
    # TODO: Parts of this code are heavily inspired by ChatGPT
    export = crud.export_all(db)

    # Write the data to a JSON file
    with open("export.json", "w") as f:
        json.dump(export, f, default=str, indent=4, ensure_ascii=False)

    # Return the file as a download
    return FileResponse("export.json", media_type="application/json", filename="export.json")


@app.delete("/purge", tags=["Import/Export/Purge Database"])
async def purge_database(db: Session = Depends(get_db)):
    """
    Purges the entire database aside from the 'users' table
    :return:
    """
    return crud.delete_all_except_users(db)


"""
####################
Device related routes
####################
"""


# ##### GET - Routes #####
@app.get("/devices", tags=["Devices"])
async def get_all_devices(db: Session = Depends(get_db)):
    # TODO: add error handling
    return crud.get_devices(db)


@app.get("/devices/{device_id}", tags=["Devices"])
async def get_device_by_id(device_id: str, db: Session = Depends(get_db)):
    # TODO: add error handling
    return crud.get_device_by_id(db, device_id)


@app.get("/devices/{device_id}/location-transactions", tags=["Devices"])
async def get_location_transactions_by_device_id(device_id: str, db: Session = Depends(get_db)):
    # TODO: Implement get_location_transactions_by_device_id
    return {"Location Transactions": "Location1"}


@app.get("/devices/{device_id}/owner-transactions", tags=["Devices"])
async def get_owner_transactions_by_device_id(device_id: str, db: Session = Depends(get_db)):
    # TODO: Implement get_owner_transactions_by_device_id
    return {"Owner Transactions": "Owner1"}


@app.get("/devices/{device_id}/purchasing-information", tags=["Devices"])
async def get_purchasing_information_by_device_id(device_id: str, db: Session = Depends(get_db)):
    # TODO: Implement get_purchasing_information_by_device_id
    return {"Purchasing Information": "Info1"}


# ##### POST - Routes #####
@app.post("/devices", tags=["Devices"])
async def new_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    return crud.create_device(db, device)


@app.post("/devices/{device_id}/location-transactions", tags=["Devices"])
async def new_location_transaction(
        location_transaction: schemas.LocationTransactionCreate,
        db: Session = Depends(get_db)
):
    # TODO: Update to new api route
    return crud.create_location_transaction(db, location_transaction)


@app.post("/devices/{device_id}/owner-transactions", tags=["Devices"])
async def new_owner_transaction(
        owner_transaction: schemas.OwnerTransactionCreate,
        db: Session = Depends(get_db)
):
    # TODO: Update to new api route
    return crud.create_owner_transaction(db, owner_transaction)


@app.post("/devices/{device_id}/purchasing-information", tags=["Devices"])
async def new_purchasing_information(
        purchasing_information: schemas.PurchasingInformationCreate, device_id: str,
        db: Session = Depends(get_db)
):
    # TODO: Review
    create_purchasing_information = crud.create_purchasing_information(db, purchasing_information, device_id)
    return create_purchasing_information


# ##### PUT - Routes #####
@app.put("/devices/{device_id}", tags=["Devices"])
async def update_device_by_id(device_id: str, db: Session = Depends(get_db)):
    # TODO: Implement update_device_by_id
    return {"Update": "Successful"}


@app.put("/devices/{device_id}/location-transactions", tags=["Devices"])
async def update_location_transaction(
        location_transaction: schemas.LocationTransactionCreate,
        db: Session = Depends(get_db)
):
    # TODO: implement
    return {"TBD": "Not yet implemented"}


@app.put("/devices/{device_id}/owner-transactions", tags=["Devices"])
async def update_owner_transaction(
        owner_transaction: schemas.OwnerTransactionCreate,
        db: Session = Depends(get_db)
):
    # TODO: implement
    return {"TBD": "Not yet implemented"}


@app.put("/devices/{device_id}/purchasing-informations", tags=["Devices"])
async def update_purchasing_information(
        purchasing_information: schemas.PurchasingInformationCreate, device_id: str,
        db: Session = Depends(get_db)
):
    # TODO: implement
    return {"TBD": "Not yet implemented"}


# ##### DELETE - Routes #####
@app.delete("/devices/{device_id}", tags=["Devices"])
async def delete_device(device_id: str, db: Session = Depends(get_db)):
    # TODO: Test exception handling
    return crud.delete_device_by_id(db, device_id)


@app.delete("/devices/{device_id}/location-transactions", tags=["Devices"])
async def delete_location_transaction_by_device_id(
        device_id: str,
        location_transaction_id: str,
        db: Session = Depends(get_db)
        ):
    # TODO: Implement
    return {"TBD": "Not yet implemented"}


@app.delete("/devices/{device_id}/owner-transactions", tags=["Devices"])
async def delete_owner_transaction_by_device_id(
        device_id: str,
        owner_transaction_id: str,
        db: Session = Depends(get_db)
        ):
    # TODO: Implement
    return {"TBD": "Not yet implemented"}


@app.delete("/devices/{device_id}/purchasing-informations", tags=["Devices"])
async def delete_purchasing_information_by_device_id(
        device_id: str,
        purchasing_information_id: str,
        db: Session = Depends(get_db)
        ):
    # TODO: Implement
    return {"TBD": "Not yet implemented"}


"""
####################
Test related routes
####################
"""


@app.get("/", response_model=schemas.Device)
def read_root(db: Session = Depends(get_db)):
    return crud.get_device_by_id(db, "a188957e-0184-4653-b950-7b98b86f8471")


@app.post("/")
def post_root(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    return crud.create_device(db, device)


@app.post("/owner-transaction")
def post_root(owner_transaction: schemas.OwnerTransactionCreate, db: Session = Depends(get_db)):
    return crud.create_owner_transaction(db, owner_transaction)


@app.get("/test/")
async def testing_auth(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@app.get("/users/", tags=["Authentication"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/by-username/{username}/", response_model=schemas.User, tags=["Authentication"])
def read_users_by_username(rz_username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, rz_username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
