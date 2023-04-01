# Creating the pydantic Models

from pydantic import BaseModel


# TODO: Add source? (https://fastapi.tiangolo.com/tutorial/security/get-current-user/#__tabbed_2_1)
class UserBase(BaseModel):
    """
    The current pydantic user schema according to the FastAPI Docs
        - Currently not using a hashed password!!!
    Attributes:
        full_name : str
        organisation_unit : str
        has_admin_privileges : bool
    """
    rz_username: str
    full_name: str
    organisation_unit: str
    has_admin_privileges: bool


class UserCreate(UserBase):
    """
    UserBase subclass for referencing the users password
    Attributes:
        hashed_password : str
    """
    hashed_password: str


class User(UserBase):
    pass

    class Config:
        orm_mode = True


class Token(BaseModel):
    """
    Token class which is used to handle the access tokens sent after login.
    Attributes:
        access_token: str
        token_type: str
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Token data class used to store the username.
    Attributes:
        rz_username: str
    """
    rz_username: str | None = None


class DeviceBase(BaseModel):
    """
    Device Base, which handles all the necessary data a device needs to have
    Attributes:
        title: str
        device_type: str
        rz_username_buyer: str
        serial_number: str
        image_url: str
    """
    title: str
    device_type: str
    rz_username_buyer: str
    serial_number: str
    image_url: str


class DeviceCreate(DeviceBase):
    """
    Device Create
    """
    pass


class Device(DeviceBase):
    """
    Device pydantic schema, which inherits all necessary attributes from Device Base.
    Configures Device for orm mode.
    Attributes:
        device_id: str
        description: str
        accessories: str
    """
    device_id: str
    description: str
    accessories: str

    class Config:
        orm_mode = True


class OwnerTransactionBase(BaseModel):
    """
    Owner transaction base, which handles all necessary data an owner transaction needs to have.
    Attributes:
        rz_username: str
        timestamp_owner_since: str
    """
    rz_username: str
    timestamp_owner_since: str


class OwnerTransactionCreate(OwnerTransactionBase):
    """
    Owner transaction create
    """
    pass


class OwnerTransaction(OwnerTransactionBase):
    """
    Owner transaction pydantic schema, which inherits all the necessary attributs from the OwnerTransactionBase-class.
    Sets orm_mode to true.
    Attributes:
        owner_transaction_id: str
    """
    owner_transaction_id: str

    class Config:
        orm_mode = True


class LocationTransactionBase(BaseModel):
    """
    Location transaction base, which handles all necessary data an location transaction needs to have.
    Attributes:
        room_code: str
        timestamp_located_since: str
    """
    room_code: str
    timestamp_located_since: str


class LocationTransactionCreate(OwnerTransactionBase):
    """
    Location transaction create
    """
    pass


class LocationTransaction(OwnerTransactionBase):
    """
    Location transaction pydantic schema,
    which inherits all the necessary attributs from the LocationTransactionBase-class.

    Sets orm_mode to true.

    Attributes:
        location_transaction_id: str
    """
    location_transaction_id: str

    class Config:
        orm_mode = True
