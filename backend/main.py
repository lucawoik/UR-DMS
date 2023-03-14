from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/test/")
async def testing_auth(token: str = Depends(oauth2_scheme)):
    return {"token": token}
