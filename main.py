from fastapi import FastAPI, HTTPException
from datetime import timedelta
import crud
import schemas
import jwt  

app = FastAPI()

# Configurações do JWT
SECRET_KEY = "seu_segredo_aqui"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/registrar/", response_model=schemas.User, tags=["Usuários"])
def create_user(user: schemas.UserCreate):
    db_user = crud.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="User already registered")

    user.hash_senha() 
    new_user = crud.create_user(user.model_dump())

    # Gerar JWT token após registro
    access_token = create_access_token(data={"sub": user.email})

    return schemas.User(
        id=new_user['id'],
        email=new_user['email'],
        name=new_user['name'],
        senha=new_user['senha'],  # Armazena o hash da senha
        access_token=access_token
    )

@app.get("/usuarios/", response_model=list[schemas.User], tags=["Usuários"])
def read_users(skip: int = 0, limit: int = 100):
    return crud.get_users(skip=skip, limit=limit)

@app.get("/usuarios/{user_id}", response_model=schemas.User, tags=["Usuários"])
def read_user(user_id: int):
    db_user = crud.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
