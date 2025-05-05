from pydantic import BaseModel
from datetime import date
from typing import Optional

# Схемы для пользователей
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    created_at: date

class User(UserBase):
    id: int
    created_at: date
    
    class Config:
        orm_mode = True

# Схемы для категорий
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

# Схемы для транзакций
class TransactionBase(BaseModel):
    amount: float
    type: str
    date: date
    category_id: int
    user_id: int

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    
    class Config:
        orm_mode = True

# Схемы для аутентификации
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str