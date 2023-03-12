# Creating the pydantic Models

from pydantic import BaseModel


class User(BaseModel):
    rz_username: str
    full_name: str
    organisation_unit: str
    has_admin_privileges: bool
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
