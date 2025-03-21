from datetime import datetime, timedelta, timezone
import jwt
from core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict) -> str:
    """
    Creates a JSON Web Token (JWT) for the given data with an expiration time.

    Args:
        data (dict): The data to be encoded into the JWT.

    Returns:
        str: The encoded JWT as a string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """
    Verifies a JWT token and decodes its payload.

    Args:
        token (str): The JWT token to be verified.

    Returns:
        dict: The decoded payload if the token is valid.
        None: If the token is invalid or an error occurs during decoding.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None