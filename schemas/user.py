from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    user_id : int
    name : str
    email: EmailStr
    password : str
    role : str
