# Creating the pydantic Models

from pydantic import BaseModel


# TODO: Add source? (https://fastapi.tiangolo.com/tutorial/security/get-current-user/#__tabbed_2_1)
class User(BaseModel):
    """ The current pydantic user schema according to the FastAPI Docs
        - Currently using a fake_hashed password!!!
    Attributes:
        rz_username:str
        full_name : str
        organisation_unit : str
        has_admin_privileges : bool
        hashed_password : str
    """
    rz_username: str
    full_name: str
    organisation_unit: str
    has_admin_privileges: bool
    # TODO: Currently using a fake hashed password instead of a securely hashed one
    fake_hashed_password: str

