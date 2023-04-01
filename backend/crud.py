import uuid

from sqlalchemy.orm import Session

from . import models, schemas


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


def get_devices(db: Session, skip: int = 0, limit: int = 100):
    """
    Get all devices from the database.
    :param db:
    :param skip:
    :param limit:
    :return:
    """
    return db.query(models.Device).offset(skip).limit(limit).all()


def get_device_by_id(db: Session, device_id: str):
    """
    Get a device from the database by id.
    :param db:
    :param device_id:
    :return:
    """
    return db.query(models.Device).filter(models.Device.device_id == device_id).first()


def create_device(db: Session, device: schemas.DeviceCreate):
    """
    Create a device according to the schema DeviceCreate and add it to the database.
    :param db:
    :param device:
    :return:
    """
    db_device = models.Device(**device.dict(), device_id=str(uuid.uuid4()))
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


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
    return db.query(models.OwnerTransaction).filter(models.OwnerTransaction.device_id == device_id)


def create_owner_transaction(db: Session, owner_transaction: schemas.OwnerTransactionCreate):
    """
    Create an owner transaction according to the schema OwnerTransactionCreate and add it to the database.
    :param db:
    :param owner_transaction:
    :return:
    """
    db_owner_transaction = models.OwnerTransaction(**owner_transaction.dict(), owner_transaction_id=str(uuid.uuid4()))
    db.add(db_owner_transaction)
    db.commit()
    db.refresh(db_owner_transaction)
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
    return db.query(models.LocationTransaction).filter(models.LocationTransaction.device_id == device_id)


def create_location_transaction(db: Session, location_transaction: schemas.LocationTransactionCreate):
    """
    Create a location transaction according to the schema LocationTransactionCreate and add it to the database.
    :param db:
    :param location_transaction:
    :return:
    """
    db_location_transaction = models.LocationTransaction(**location_transaction.dict(), location_transaction_id=str(uuid.uuid4()))
    db.add(db_location_transaction)
    db.commit()
    db.refresh(db_location_transaction)
    return location_transaction


def get_purchasing_information_by_device_id(db: Session, device_id: str):
    return db.query(models.PurchasingInformation).filter(models.PurchasingInformation.device_id == device_id)


def create_purchasing_information(db: Session, purchasing_information: schemas.PurchasingInformationCreate):
    db_purchasing_information = models.PurchasingInformation(**purchasing_information.dict(),
                                                             purchasing_information_id=str(uuid.uuid4()))
