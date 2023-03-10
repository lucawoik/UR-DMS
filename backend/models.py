from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User:
    """DB-Model class for the 'users' table.
    Attributes:
        rz_username : str (PK)
        full_name : str
        organisation_unit : str
        has_admin_privileges : bool
        hashed_password : str
    """

class Device:
    """DB-Model class for 'devices' table
    Attributes:
        device_id : str (PK)
        title : str
        device_type : str
        description : str
        accessories : str
        rz_username_buyer : str
        serial_number : str
        image_url : str
    """

class OwnerTransaction:
    """DB-Model class for 'owner_transactions' table
    Attributes:
        owner_transaction_id: str (PK)
        rz_username : str
        timestamp_owner_since : str
        device_id : str (FK)
    """

class LocationTransaction:
    """DB-Model class for 'location_transactions' table
    Attributes:
        location_transaction_id : str (PK)
        room_code : str
        timestamp_located_since : str
        device_id : str (FK)
    """

class PurchasingInformation:
    """DB-Model class for  'purchasing_information' table
    Attributes:
        purchasing_information_id : str (PK)
        price : str
        timestamp_warranty_end : str
        timestamp_purchase : str
        cost_centre :int
        seller : str
        device_id : str (FK)
    """
