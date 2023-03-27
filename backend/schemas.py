# Creating the pydantic Models

from pydantic import BaseModel


# TODO: Add source? (https://fastapi.tiangolo.com/tutorial/security/get-current-user/#__tabbed_2_1)


class User(BaseModel):
    """ The current pydantic user schema according to the FastAPI Docs
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
