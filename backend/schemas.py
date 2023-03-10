# Creating the pydantic Models

from pydantic import BaseModel


class UserBase(BaseModel):
    full_name: str
    organisation_unit: str
    has_admin_privileges: bool


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    rz_username: str
