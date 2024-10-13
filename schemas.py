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
        self.senha = bcrypt.hashpw(self.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    senha: Optional[str] = None

    # Hash da senha no momento da atualização, se uma nova senha for fornecida
    def hash_senha(self):
        if self.senha:
            self.senha = bcrypt.hashpw(self.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

class User(UserBase):
    id: int
    senha: str  # Armazena o hash da senha no banco
    access_token: str  # Novo campo para o token de acesso

    class Config:
        from_attributes = True
