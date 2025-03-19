from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from core.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from models.models import select_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
#     payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
#     email = payload.get("sub")
#     if email is None:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     user = db.exec(select(User).where(User.email == email)).first()
#     if not user:
#         raise HTTPException(status_code=401, detail="User not found")

#     return user

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_data = select_user(email)
        # # 🔥 Connexion à la base SQLite
        # conn = sqlite3.connect(DATABASE_PATH)
        # cursor = conn.cursor()
        
        # # 🛠 Exécution de la requête SQL brute pour récupérer l'utilisateur
        # cursor.execute("SELECT id, email, hashed_password, role FROM users WHERE email = ?", (email,))
        # user_data = cursor.fetchone()
        
        # conn.close()

        if user_data is None:
            raise HTTPException(status_code=401, detail="User not found")

        # Retourner un dictionnaire représentant l'utilisateur
        return {
            "id": user_data[0],
            "name": user_data[1],
            "email": user_data[2],
            "hashed_password": user_data[3],
            "role": user_data[4]
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
