from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pymongo.errors import DuplicateKeyError

from .settings import settings
from mongo.connect import get_collection
from app_base.models.models import UserCreate, UserLogin, Token, User

router = APIRouter(tags=["authentication"])
## chang to get_collection("users")
users_collection = get_collection("users")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_password_hash(password: str) -> str:
    """
    Hash the password using bcrypt
    """
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pw.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify the password against the hash
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_user(username: str) -> Optional[Dict[str, Any]]:
    """
    Get a user from the database by username
    """
    user = users_collection.find_one({"username": username})
    return user

def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate a user
    """
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify a JWT token and return the payload if valid
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        return {"username": username}
    except JWTError:
        return None

@router.post("/api/register", response_model=User)
async def register_user(user: UserCreate):
    """
    Register a new user
    """
    try:
        hashed_password = get_password_hash(user.password)
        new_user = {
            "username": user.username,
            "email": user.email,
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow()
        }
        
        result = users_collection.insert_one(new_user)
        new_user["id"] = str(result.inserted_id)
        del new_user["hashed_password"]
        
        return new_user
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

@router.post("/register-form")
async def register_form(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    """
    Handle registration form submission
    """
    try:
        user = UserCreate(username=username, email=email, password=password)
        await register_user(user)
        request.session["message"] = "Registration successful! Please login."
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    except HTTPException as e:
        request.session["error"] = e.detail
        return RedirectResponse(url="/register", status_code=status.HTTP_303_SEE_OTHER)
    except ValueError as e:
        request.session["error"] = str(e)
        return RedirectResponse(url="/register", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/api/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login and get access token
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login-form")
async def login_form(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    """
    Handle login form submission
    """
    try:
        print("<<<<----Login form", username, password)
        form_data = OAuth2PasswordRequestForm(username=username, password=password)
        token = await login_for_access_token(form_data)
        request.session["token"] = token["access_token"]# token.access_token
        request.session["username"] = username
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    except HTTPException as e:
        request.session["error"] = e.detail
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/api/users/me", response_model=User)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get the current authenticated user
    """
    credentials = verify_token(token)
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = get_user(credentials["username"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"]
    }

@router.get("/logout")
async def logout(request: Request):
    """
    Logout the user
    """
    if "token" in request.session:
        del request.session["token"]
    if "username" in request.session:
        del request.session["username"]
    
    return RedirectResponse(url="/login")