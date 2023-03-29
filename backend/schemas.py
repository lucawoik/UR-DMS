# Creating the pydantic Models

from pydantic import BaseModel


<<<<<<< HEAD
class User(BaseModel):
=======
# TODO: Add source? (https://fastapi.tiangolo.com/tutorial/security/get-current-user/#__tabbed_2_1)


class User(BaseModel):
    """ The current pydantic user schema according to the FastAPI Docs
        - Currently not using a hashed password!!!
    Attributes:
        full_name : str
        organisation_unit : str
        has_admin_privileges : bool
    """
>>>>>>> origin/main
    rz_username: str
    full_name: str
    organisation_unit: str
    has_admin_privileges: bool
<<<<<<< HEAD
    hashed_password: str


class Device(BaseModel):
    device_id: str
    title: str
    device_type: str
    description: str
    accessories: str
    rz_username_buyer: str
    serial_number: str
    image_url: str


class OwnerTransaction(BaseModel):
    owner_transaction_id: str
    rz_username: str
    timestamp_owner_since: str
    device_id: str


class LocationTransaction(BaseModel):
    location_transaction_id: str
    room_code: str
    timestamp_located_since: str
    device_id: str


class PurchasingInformation(BaseModel):
    purchasing_information_id: str
    price: str
    timestamp_warranty_end: str
    timestamp_purchase: str
    cost_centre: int
    seller: str
    device_id: str
=======
    # TODO: Add hashed password Currently not using a password

    class Config:
        orm_mode = True


class UserCreate(User):
    """UserBase subclass for referencing the users password
    Attributes:
        hashed_password : str
    """
    hashed_password: str


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
        username: str
    """
    rz_username: str | None = None
>>>>>>> origin/main
