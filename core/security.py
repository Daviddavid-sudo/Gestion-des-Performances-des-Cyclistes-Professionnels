from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from core.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from models.models import select_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if the provided plain password matches the hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashes a given password using a predefined password hashing context.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Creates a JSON Web Token (JWT) for the given data with an optional expiration time.

    Args:
        data (dict): The data to encode into the token.
        expires_delta (timedelta, optional): The time duration after which the token will expire. 
                                             If not provided, a default expiration time is used.

    Returns:
        str: The encoded JWT as a string.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Retrieve the current user based on the provided JWT token.

    Args:
        token (str): The JWT token provided by the user.

    Returns:
        dict: A dictionary containing user information such as id, name, email, hashed_password, and role.

    Raises:
        HTTPException: If the token is invalid, the user is not found, or credentials could not be validated.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_data = select_user(email)

        if user_data is None:
            raise HTTPException(status_code=401, detail="User not found")

        return {
            "id": user_data[0],
            "name": user_data[1],
            "email": user_data[2],
            "hashed_password": user_data[3],
            "role": user_data[4]
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
