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
    db_device = models.Device(device_id=str(uuid.uuid4()),
                              title=device.title,
                              device_type=device.device_type,
                              description=device.description,
                              accessories=device.accessories,
                              rz_username_buyer=device.rz_username_buyer,
                              serial_number=device.serial_number,
                              image_url=device.image_url
                              )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device
