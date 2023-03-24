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
