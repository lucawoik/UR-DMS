import sqlalchemy.exc
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas


"""
####################
CREATE
####################
"""


def create_user(db: Session, user: schemas.UserCreate):
    """
    Create a new user according to the User model and commit it to the database
    :param db:
    :param user:
    :return:
    """
    db_user = models.User(rz_username=user.rz_username,
                          full_name=user.full_name,
                          organisation_unit=user.organisation_unit,
                          has_admin_privileges=user.has_admin_privileges,
                          hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_device(db: Session, device: schemas.DeviceCreate):
    """
    Create a device according to the schema DeviceCreate and add it to the database.
    :param db:
    :param device:
    :return:
    """
    db_device = models.Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


def create_owner_transaction(db: Session, device_id: str, owner_transaction: schemas.OwnerTransactionCreate):
    """
    Create an owner transaction according to the schema OwnerTransactionCreate and add it to the database.
    :param db:
    :param device_id:
    :param owner_transaction:
    :return:
    """
    db_owner_transaction = models.OwnerTransaction(device_id=device_id, **owner_transaction.dict())
    db_owner_transaction.devices = get_device_by_id(db, device_id)
    db.add(db_owner_transaction)
    db.commit()
    db.refresh(db_owner_transaction)
    return db_owner_transaction


def create_location_transaction(db: Session, device_id: str, location_transaction: schemas.LocationTransactionCreate):
    """
    Create a location transaction according to the schema LocationTransactionCreate and add it to the database.
    :param db:
    :param device_id:
    :param location_transaction:
    :return:
    """
    db_location_transaction = models.LocationTransaction(device_id=device_id, **location_transaction.dict())
    db_location_transaction.devices = get_device_by_id(db, device_id)
    db.add(db_location_transaction)
    db.commit()
    db.refresh(db_location_transaction)
    return db_location_transaction


def create_purchasing_information(db: Session, device_id: str, purchasing_information: schemas.PurchasingInformationCreate):
    """
    Create a purchasing information entry according to the schema PurchasingInformationCreate and add it to the
    database.
    :param db:
    :param device_id:
    :param purchasing_information:
    :return:
    """
    db_purchasing_information = models.PurchasingInformation(device_id=device_id, **purchasing_information.dict())
    db_purchasing_information.devices = get_device_by_id(db, device_id)
    db.add(db_purchasing_information)
    db.commit()
    db.refresh(db_purchasing_information)
    return db_purchasing_information


def import_json(db: Session, data: dict):
    """
    Function to import a compatible dict onto the existing db.
    :param data:
    :param db:
    :return:
    """
    try:
        for item in data["devices"]:
            device = schemas.DeviceCreate(**item)
            create_device(db, device)
        for item in data["owner_transactions"]:
            owner_transaction = schemas.OwnerTransactionCreate(**item)
            device_id = item["device_id"]
            create_owner_transaction(db, device_id, owner_transaction)
        for item in data["location_transactions"]:
            location_transaction = schemas.LocationTransactionCreate(**item)
            device_id = item["device_id"]
            create_location_transaction(db, device_id, location_transaction)
        for item in data["purchasing_information"]:
            purchasing_information = schemas.PurchasingInformationCreate(**item)
            device_id = item["device_id"]
            create_purchasing_information(db, device_id, purchasing_information)
        return status.HTTP_201_CREATED
    except sqlalchemy.exc.IntegrityError:
        return status.HTTP_409_CONFLICT


"""
####################
READ
####################
"""


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Method, which gets all the users from the database
    :param db:
    :param skip:
    :param limit:
    :return:
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_username(db: Session, rz_username: str):
    """
    Get a user from the DB according to the username
    :param db:
    :param rz_username:
    :return:
    """
    return db.query(models.User).filter(models.User.rz_username == rz_username).first()


def get_devices(db: Session):
    """
    Get all devices from the database.
    :param db:
    :param skip:
    :param limit:
    :return:
    """
    return db.query(models.Device).all()


def get_device_by_id(db: Session, device_id: str):
    """
    Get a device from the database by id.
    :param db:
    :param device_id:
    :return:
    """
    return db.query(models.Device).filter(models.Device.device_id == device_id).first()


def get_owner_transactions(db: Session):
    """
    Get all owner transactions from the database.
    :param db:
    :return:
    """
    return db.query(models.OwnerTransaction).all()


def get_owner_transaction_by_device_id(db: Session, device_id: str):
    """
    Get an owner transaction by device id.
    :param db:
    :param device_id:
    :return:
    """
    return db.query(models.OwnerTransaction).filter(models.OwnerTransaction.device_id == device_id).all()


def get_owner_transaction_by_id(db: Session, owner_transaction_id: str):
    """
    Returns the owner transaction matching the given ID.
    :param db:
    :param owner_transaction_id:
    :return:
    """
    owner_transaction = db.query(models.OwnerTransaction).\
        filter(models.OwnerTransaction.owner_transaction_id == owner_transaction_id).first()
    if not owner_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="An owner transaction with this ID does not exist."
        )
    return owner_transaction


def get_location_transactions(db: Session):
    """
    Get all location transactions from the database.
    :param db:
    :return:
    """
    return db.query(models.LocationTransaction).all()


def get_location_transaction_by_device_id(db: Session, device_id: str):
    """
    Get a location transaction by device id.
    :param db:
    :param device_id:
    :return:
    """
    return db.query(models.LocationTransaction).filter(models.LocationTransaction.device_id == device_id).all()


def get_location_transaction_by_id(db: Session, location_transaction_id: str):
    """
    Returns the location transaction matching the given ID.
    :param db:
    :param location_transaction_id:
    :return:
    """
    location_transaction = db.query(models.LocationTransaction).\
        filter(models.LocationTransaction.location_transaction_id == location_transaction_id).first()
    if not location_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="A location transaction with this ID does not exist."
        )
    return location_transaction


def get_purchasing_information_by_device_id(db: Session, device_id: str):
    """
    Find purchasing information for specific device using the device_id
    :param db:
    :param device_id:
    :return:
    """
    return db.query(models.PurchasingInformation).filter(models.PurchasingInformation.device_id == device_id).all()


def get_purchasing_information_by_id(db: Session, purchasing_information_id: str):
    """
    Returns the purchasing information matching the given ID.
    :param db:
    :param purchasing_information_id:
    :return:
    """
    purchasing_information = db.query(models.PurchasingInformation).\
        filter(models.PurchasingInformation.purchasing_information_id == purchasing_information_id).first()
    if not purchasing_information:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="A purchasing information with this ID does not exist."
        )
    return purchasing_information


def export_all(db: Session):
    """
    Exporting data from Database (except 'users' table) as a dict.
    :param db:
    :return:
    """
    # TODO: Parts of this code are heavily inspired by ChatGPT
    export_dict = {
        "devices": [],
        "owner_transactions": [],
        "location_transactions": [],
        "purchasing_information": []
    }
    devices_list = db.query(models.Device).all()
    for device in devices_list:
        device_dict = device.__dict__
        device_dict.pop("_sa_instance_state", None)
        export_dict["devices"].append(device_dict)
    owner_transactions_list = db.query(models.OwnerTransaction).all()
    for owner_transaction in owner_transactions_list:
        owner_transaction_dict = owner_transaction.__dict__
        owner_transaction_dict.pop("_sa_instance_state", None)
        export_dict["owner_transactions"].append(owner_transaction_dict)
    location_transactions_list = db.query(models.LocationTransaction).all()
    for location_transaction in location_transactions_list:
        location_transaction_dict = location_transaction.__dict__
        location_transaction_dict.pop("_sa_instance_state", None)
        export_dict["location_transactions"].append(location_transaction_dict)
    purchasing_information_list = db.query(models.PurchasingInformation).all()
    for purchasing_information in purchasing_information_list:
        purchasing_information_dict = purchasing_information.__dict__
        purchasing_information_dict.pop("_sa_instance_state", None)
        export_dict["purchasing_information"].append(purchasing_information_dict)
    return export_dict


"""
####################
UPDATE
####################
"""


def update_device(db: Session, device: models.Device, updated_device: schemas.DeviceUpdate):
    """
    Updating device with given updates.
    :param db:
    :param device:
    :param updated_device:
    :return:
    """
    updating_dict = updated_device.dict(exclude_none=True)  # excluding empty attributes from the dict
    for key in updating_dict:
        device.__setattr__(key, updating_dict[key])
    db.commit()
    return get_device_by_id(db, device.device_id)


def update_owner_transaction(db: Session,
                             owner_transaction_id: str,
                             updated_transaction: schemas.OwnerTransactionUpdate
                             ):
    """
    Updating a certain owner transaction with given updates.
    :param db:
    :param owner_transaction_id:
    :param updated_transaction:
    :return:
    """
    to_update = get_owner_transaction_by_id(db, owner_transaction_id)
    updating_dict = updated_transaction.dict(exclude_none=True)
    for key in updating_dict:
        to_update.__setattr__(key, updating_dict[key])
    db.commit()
    return get_owner_transaction_by_id(db, owner_transaction_id)


def update_location_transaction(db: Session,
                                location_transaction_id: str,
                                updated_transaction: schemas.LocationTransactionUpdate
                                ):
    """
    Updating a certain location transaction with given updates.
    :param db:
    :param location_transaction_id:
    :param updated_transaction:
    :return:
    """
    to_update = get_location_transaction_by_id(db, location_transaction_id)
    updating_dict = updated_transaction.dict(exclude_none=True)
    for key in updating_dict:
        to_update.__setattr__(key, updating_dict[key])
    db.commit()
    return get_location_transaction_by_id(db, location_transaction_id)


def update_purchasing_information(db: Session,
                                  purchasing_information_id: str,
                                  updated_information: schemas.PurchasingInformationUpdate
                                  ):
    """
    Updating a certain purchasing information with given updates.
    :param db:
    :param purchasing_information_id:
    :param updated_information:
    :return:
    """
    to_update = get_purchasing_information_by_id(db, purchasing_information_id)
    updating_dict = updated_information.dict(exclude_none=True)
    for key in updating_dict:
        to_update.__setattr__(key, updating_dict[key])
    db.commit()
    return get_purchasing_information_by_id(db, purchasing_information_id)


"""
####################
DELETE
####################
"""


def delete_device_by_id(db: Session, device_id: str):
    """
    Get a device from the database by id.
    :param db:
    :param device_id:
    :return:
    """
    device_to_delete = get_device_by_id(db, device_id)
    if not device_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This device does not exist."
        )
    db.delete(device_to_delete)
    db.commit()
    return status.HTTP_200_OK


def delete_all_except_users(db: Session):
    """
    Deletes all content from the tables Device, OwnerTransaction, LocationTransaction and Purchasing information.
    :param db:
    :return:
    """
    db.query(models.Device).delete()
    db.query(models.OwnerTransaction).delete()
    db.query(models.LocationTransaction).delete()
    db.query(models.PurchasingInformation).delete()
    db.commit()
    return True
