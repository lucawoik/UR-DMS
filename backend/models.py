# Creating the sqlalchemy Models

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    """
    DB-Model class for the 'users' table.
    Attributes:
        rz_username : str (PK)
        full_name : str
        organisation_unit : str
        has_admin_privileges : bool
        hashed_password : str
    """
    __tablename__ = "users"

    rz_username = Column(String, primary_key=True)
    full_name = Column(String, unique=True)
    organisation_unit = Column(String)
    has_admin_privileges = Column(Boolean)
    hashed_password = Column(String)


class Device(Base):
    """
    DB-Model class for 'devices' table
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
    __tablename__ = "devices"

    device_id = Column(String, primary_key=True)
    title = Column(String)
    device_type = Column(String)
    description = Column(String, nullable=True)
    accessories = Column(String, nullable=True)
    rz_username_buyer = Column(String)
    serial_number = Column(String)
    image_url = Column(String)

    owner_transactions = relationship("OwnerTransaction", back_populates="devices")


class OwnerTransaction(Base):
    """
    DB-Model class for 'owner_transactions' table
    Attributes:
        owner_transaction_id: str (PK)
        rz_username : str
        timestamp_owner_since : str
        device_id : str (FK)
    """
    __tablename__ = "owner_transactions"

    owner_transaction_id = Column(String, primary_key=True)
    rz_username = Column(String)
    timestamp_owner_since = Column(String)

    device_id = Column(String, ForeignKey("devices.device_id"))
    devices = relationship("Device", back_populates="owner_transactions")


class LocationTransaction(Base):
    """
    DB-Model class for 'location_transactions' table
    Attributes:
        location_transaction_id : str (PK)
        room_code : str
        timestamp_located_since : str
        device_id : str (FK)
    """
    __tablename__ = "location_transactions"

    location_transaction_id = Column(String, primary_key=True)
    room_code = Column(String)
    timestamp_located_since = Column(String)
    # TODO: device_id = relationship("Device")


class PurchasingInformation(Base):
    """
    DB-Model class for  'purchasing_information' table
    Attributes:
        purchasing_information_id : str (PK)
        price : str
        timestamp_warranty_end : str
        timestamp_purchase : str
        cost_centre :int
        seller : str
        device_id : str (FK)
    """
    __tablename__ = "purchasing_information"

    purchasing_information_id = Column(String, primary_key=True)
    price = Column(String)
    timestamp_warranty_end = Column(String)
    timestamp_purchase = Column(String)
    cost_centre = Column(Integer, nullable=True)
    seller = Column(String)
    # TODO: device_id = relationship("Device")
