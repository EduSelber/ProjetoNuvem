from pydantic import BaseModel, Field
from typing import Optional
import bcrypt

class UserBase(BaseModel):
    email: str = Field(title="email", description="Email do usuário", example="cloud@insper.edu.br")
    name: str = Field(title="name", description="Nome do usuário", example="Cloud")

class UserCreate(UserBase):
    senha: str = Field(title="senha", description="Senha do usuário", example="123456")

    # Hash da senha no momento da criação
    def hash_senha(self):
        self.senha = bcrypt.hashpw(self.senha.encode('utf-8'), bcrypt.gensalt())

class User(BaseModel):
   
    email: str
    senha: str 

    class Config:
        from_attributes = True