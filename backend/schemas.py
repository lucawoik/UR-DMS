# Creating the pydantic Models
import uuid

from pydantic import BaseModel

from backend import helpers


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
        description: str
        accessories: str
        rz_username_buyer: str
        serial_number: str
        image_url: str
    """
    title: str
    device_type: str
    description: str | None = None
    accessories: str | None = None
    rz_username_buyer: str
    serial_number: str
    image_url: str


class DeviceCreate(DeviceBase):
    """
    Device Create.
    Automatically creates a uuid if none is given.
    Attributes:
        device_id: str
    """
    device_id: str | None = helpers.get_uuid()
    pass


class Device(DeviceBase):
    """
    Device pydantic schema, which inherits all necessary attributes from Device Base.
    Configures Device for orm mode.
    """
    pass

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
    Automatically creates a uuid if none is given.
    Attributes:
        device_id: str
        owner_transaction_id: str
    """
    device_id: str
    owner_transaction_id: str | None = helpers.get_uuid()
    pass


class OwnerTransaction(OwnerTransactionBase):
    """
    Owner transaction pydantic schema, which inherits all the necessary attributs from the OwnerTransactionBase-class.
    Sets orm_mode to true.
    """
    pass

    class Config:
        orm_mode = True


class LocationTransactionBase(BaseModel):
    """
    Location transaction base, which handles all necessary data a location transaction needs to have.
    Attributes:
        room_code: str
        timestamp_located_since: str
    """
    room_code: str
    timestamp_located_since: str


class LocationTransactionCreate(LocationTransactionBase):
    """
    Location transaction create.
    Automatically creates a uuid if none is given.
    Attributes:
        device_id: str
        location_transaction_id: str
    """
    device_id: str
    location_transaction_id: str | None = helpers.get_uuid()
    pass


class LocationTransaction(LocationTransactionBase):
    """
    Location transaction pydantic schema,
    which inherits all the necessary attributs from the LocationTransactionBase-class.

    Sets orm_mode to true.
    """
    pass

    class Config:
        orm_mode = True


class PurchasingInformationBase(BaseModel):
    """
    Purchasing information base, which handles all necessary data purchasing information needs to have.
    Attributes:
        price: str
        timestamp_warranty_end: str
        timestamp_purchase: str
        seller: str
    """
    price: str
    timestamp_warranty_end: str
    timestamp_purchase: str
    cost_centre: str | None = None
    seller: str


class PurchasingInformationCreate(PurchasingInformationBase):
    """
    Purchasing information create
    Automatically creates a uuid if none is given.
    Attributes:
        purchasing_information_id: str
    """
    purchasing_information_id: str | None = helpers.get_uuid()
    pass


class PurchasingInformationImport(PurchasingInformationBase):
    """
    Purchasing information import, used for importing.
    Automatically creates a uuid if none is given.
    Attributes:
        purchasing_information_id: str
        device_id: str
    """
    purchasing_information_id: str | None = helpers.get_uuid()
    device_id: str
    pass


class PurchasingInformation(PurchasingInformationBase):
    """
    Purchasing infromation pydantic schema,
    which inherits all the necessary attributs from the PurchasingInformationBase-class.

    Sets orm_mode to true.

    Attributes:
        device_id: str
    """
    device_id: str

    class Config:
        orm_mode = True
