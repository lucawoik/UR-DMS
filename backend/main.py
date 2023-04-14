import json
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import variables, helpers
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


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    """
    Get the current user by checking their token.
    Source: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
    :param token:
    :param db:
    :return:
    """
    try:
        payload = jwt.decode(token, variables.SECRET_KEY, algorithms=[variables.ALGORITHM])
        rz_username: str = payload.get("sub")
        if rz_username is None:
            raise helpers.credentials_exception
        token_data = schemas.TokenData(rz_username=rz_username)
    except JWTError:
        raise helpers.credentials_exception
    user = crud.get_user_by_username(db, rz_username=token_data.rz_username)
    if user is None:
        raise helpers.credentials_exception
    return user


async def get_current_user_is_admin(current_user: Annotated[models.User, Depends(get_current_user)]):
    """
    Checking if the current user has admin privileges.
    Source: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
    :param current_user:
    :return:
    """
    if not current_user.has_admin_privileges:
        raise HTTPException(status_code=400, detail="User has no admin privileges.")
    return current_user


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
async def read_users_me(current_user: Annotated[models.User, Depends(get_current_user)]):
    """
    Returns the currently authenticated user using the token given from oauth2
    :param: current_user:
    :return:
    """
    return current_user


@app.post("/import", tags=["Import/Export/Purge Database"])
async def import_database_json(file: UploadFile, db: Session = Depends(get_db)):
    """
    Takes a .json file and imports it onto the existing database.
        - Existing entries in the database are not deleted
        - Merge conflicts are ignored
    :return:
    TODO: Add exception handling (e.g. false json format...
    """
    data = json.loads(await file.read())
    response = crud.import_json(db, data)
    if response == status.HTTP_201_CREATED:
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
    """
    Returns all devices in the database.
    :param db:
    :return:
    """
    all_devices = crud.get_devices(db)
    if not all_devices:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No devices in the database."
        )
    return crud.get_devices(db)


@app.get("/devices/{device_id}", tags=["Devices"])
async def get_device_by_id(device_id: str, db: Session = Depends(get_db)):
    """
    Returns a specific device, which is selected by the device_id.
    :param device_id:
    :param db:
    :return:
    """
    device = crud.get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="A device with this ID does not exist."
        )
    return device


@app.get("/devices/{device_id}/owner-transactions", tags=["Devices"])
async def get_owner_transactions_by_device_id(db: Session = Depends(get_db),
                                              device: models.Device = Depends(get_device_by_id)
                                              ):
    """
    Returns all owner transactions associated with a device.
    :param db:
    :param device:
    :return:
    """
    owner_transactions = crud.get_owner_transaction_by_device_id(db, device.device_id)
    if not owner_transactions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no owner transactions associated with this device."
        )
    return owner_transactions


@app.get("/devices/{device_id}/location-transactions", tags=["Devices"])
async def get_location_transactions_by_device_id(db: Session = Depends(get_db),
                                                 device: models.Device = Depends(get_device_by_id)):
    """
    Returns all location transactions associated with a device.
    :param db:
    :param device:
    :return:
    """
    location_transactions = crud.get_location_transaction_by_device_id(db, device.device_id)
    if not location_transactions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no location transactions associated with this device."
        )
    return location_transactions


@app.get("/devices/{device_id}/purchasing-information", tags=["Devices"])
async def get_purchasing_information_by_device_id(db: Session = Depends(get_db),
                                                  device: models.Device = Depends(get_device_by_id)):
    """
    Returns the purchasing information associated with a device
    :param db:
    :param device:
    :return:
    """
    purchasing_information = crud.get_purchasing_information_by_device_id(db, device.device_id)
    if not purchasing_information:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no purchasing information associated with this device."
        )
    return purchasing_information


# ##### POST - Routes #####
@app.post("/devices", tags=["Devices"])
async def new_device(device: schemas.DeviceCreate,
                     current_user: Annotated[models.User, Depends(get_current_user)],
                     db: Session = Depends(get_db)
                     ):
    return crud.create_device(db, device)


@app.post("/devices/{device_id}/owner-transactions", status_code=status.HTTP_201_CREATED, tags=["Devices"])
async def new_owner_transaction(
        owner_transaction: schemas.OwnerTransactionCreate,
        current_user: Annotated[models.User, Depends(get_current_user)],
        db: Session = Depends(get_db),
        device: models.Device = Depends(get_device_by_id)
):
    """
    Creates a new owner transaction for the device with the given device_id.
    Uses a device dependency to ensure the device exists.
    :param owner_transaction:
    :param current_user:
    :param db:
    :param device:
    :return:
    """
    create_owner_transaction = crud.create_owner_transaction(db, device.device_id, owner_transaction)
    return create_owner_transaction


@app.post("/devices/{device_id}/location-transactions", status_code=status.HTTP_201_CREATED, tags=["Devices"])
async def new_location_transaction(
        location_transaction: schemas.LocationTransactionCreate,
        current_user: Annotated[models.User, Depends(get_current_user)],
        db: Session = Depends(get_db),
        device: models.Device = Depends(get_device_by_id)
):
    """
        Creates a new location transaction for the device with the given device_id.
        Uses a device dependency to ensure the device exists.
        :param current_user:
        :param location_transaction:
        :param db:
        :param device:
        :return:
        """
    create_location_transaction = crud.create_location_transaction(db, device.device_id, location_transaction)
    return create_location_transaction


@app.post("/devices/{device_id}/purchasing-information", status_code=status.HTTP_201_CREATED, tags=["Devices"])
async def new_purchasing_information(
        purchasing_information: schemas.PurchasingInformationCreate,
        current_user: Annotated[models.User, Depends(get_current_user)],
        db: Session = Depends(get_db),
        device: models.Device = Depends(get_device_by_id)
):
    """
        Creates a new purchasing information entry for the device with the given device_id.
        Uses a device dependency to ensure the device exists.
        :param current_user:
        :param purchasing_information:
        :param db:
        :param device:
        :return:
        """
    create_purchasing_information = crud.create_purchasing_information(db, device.device_id, purchasing_information)
    return create_purchasing_information


# ##### PUT - Routes #####
@app.put("/devices/{device_id}", tags=["Devices"])
async def update_device_by_id(update_device: schemas.DeviceUpdate, db: Session = Depends(get_db), device: models.Device = Depends(get_device_by_id),):
    """
    Updating device using the DeviceUpdate schema to validate update data.
    :param update_device:
    :param db:
    :param device:
    :return:
    """
    updated_device = crud.update_device(db, device, update_device)
    if not updated_device:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The update was not possible."
        )
    return updated_device


@app.put("/devices/{device_id}/owner-transactions/{transaction_id}", tags=["Devices"])
async def update_owner_transaction(
        device_id: str,
        transaction_id: str,
        update_transaction: schemas.OwnerTransactionUpdate,
        db: Session = Depends(get_db)
):
    """
    Updating a certain owner transaction using the OwnerTransactionUpdate schema.
    :param device_id:
    :param transaction_id:
    :param update_transaction:
    :param db:
    :return:
    """
    await get_device_by_id(device_id, db)
    updated_transaction = crud.update_owner_transaction(db, transaction_id, update_transaction)
    return updated_transaction


@app.put("/devices/{device_id}/location-transactions/{transaction_id}", tags=["Devices"])
async def update_location_transaction(
        device_id: str,
        transaction_id: str,
        update_transaction: schemas.LocationTransactionUpdate,
        db: Session = Depends(get_db)
):
    """
        Updating a certain owner transaction using the OwnerTransactionUpdate schema.
        :param device_id:
        :param transaction_id:
        :param update_transaction:
        :param db:
        :return:
        """
    await get_device_by_id(device_id, db)
    updated_transaction = crud.update_location_transaction(db, transaction_id, update_transaction)
    return updated_transaction


@app.put("/devices/{device_id}/purchasing-information/{information_id}", tags=["Devices"])
async def update_purchasing_information(
        device_id: str,
        information_id: str,
        update_information: schemas.PurchasingInformationUpdate,
        db: Session = Depends(get_db)
):
    """
    Updating a certain purchasing information entry using PurchasingInformationUpdate schema.
    :param device_id:
    :param information_id:
    :param update_information:
    :param db:
    :return:
    """
    await get_device_by_id(device_id, db)
    updated_information = crud.update_purchasing_information(db, information_id, update_information)
    return updated_information


# ##### DELETE - Routes #####
@app.delete("/devices/{device_id}", tags=["Devices"])
async def delete_device(db: Session = Depends(get_db), device: models.Device = Depends(get_device_by_id)):
    return crud.delete_device_by_id(db, device.device_id)


@app.delete("/devices/{device_id}/owner-transactions/{transaction_id}", tags=["Devices"])
async def delete_owner_transaction_by_device_id(
        device_id: str,
        owner_transaction_id: str,
        db: Session = Depends(get_db)
        ):
    """
    Delete a ceratin owner transaction entry by its ID given in the URL.
    :param device_id:
    :param owner_transaction_id:
    :param db:
    :return:
    """
    await get_device_by_id(device_id, db)
    return crud.delete_owner_transaction(db, owner_transaction_id)


@app.delete("/devices/{device_id}/location-transactions/{transaction_id}", tags=["Devices"])
async def delete_location_transaction_by_device_id(
        device_id: str,
        location_transaction_id: str,
        db: Session = Depends(get_db)
        ):
    """
    Delete a ceratin location transaction entry by its ID given in the URL.
    :param device_id:
    :param location_transaction_id:
    :param db:
    :return:
    """
    await get_device_by_id(device_id, db)
    return crud.delete_location_transaction(db, location_transaction_id)


@app.delete("/devices/{device_id}/purchasing-information/{information_id}", tags=["Devices"])
async def delete_purchasing_information_by_device_id(
        device_id: str,
        purchasing_information_id: str,
        db: Session = Depends(get_db)
        ):
    """
    Delete a ceratin purchasing information entry by its ID given in the URL.
    :param device_id:
    :param purchasing_information_id:
    :param db:
    :return:
    """
    await get_device_by_id(device_id, db)
    return crud.delete_purchasing_information(db, purchasing_information_id)


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
