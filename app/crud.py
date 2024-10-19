from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
from passlib.context import CryptContext

# Contexto para hashing de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para verificar hash da senha


# Retorna o usuário pelo ID
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Retorna o usuário pelo email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Retorna os usuários armazenados
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

# Cria um novo usuário
def create_user(db: Session, user: UserCreate):
    # Verifica se já existe um usuário com o mesmo email
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise ValueError("Email já cadastrado")  # Você pode personalizar esta exceção

    # Hash da senha antes de armazenar no banco
    

    db_user = User(
        email=user.email,
        name=user.name,
        hashed_password=user.senha  # Armazena a senha com hash
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
