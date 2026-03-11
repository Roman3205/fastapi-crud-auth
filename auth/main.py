from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, utils
from database import get_db
from dotenv import load_dotenv
from os import getenv
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_MINS = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINS)
    to_encode.update({'exp': expire})
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token

app = FastAPI()

@app.post('/signup')
def register_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with provided email already existing")

    hashed_password = utils.hash_password(user.password)
    new_user = models.User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_password,
        role = user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh()

    return {
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email,
        'role': new_user.role
    }

@app.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")

    if not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    token_payload = {'sub': user.email, 'role': user.role}
    token = create_access_token(token_payload)
    return {"access_token": token, "token_type": "bearer"}

# def get_current_user(token: str = Depends(oauth2_scheme)):