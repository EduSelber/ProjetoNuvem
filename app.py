from fastapi import FastAPI, HTTPException
import crud
import schemas

app = FastAPI()

################################################### CRUD para Usuários ###################################################

@app.post("/usuarios/", response_model=schemas.User, tags=["Usuários"])
def create_user(user: schemas.UserCreate):
    db_user = crud.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    
    user.hash_senha()  # Hash da senha
    return crud.create_user(user.model_dump())

@app.get("/usuarios/", response_model=list[schemas.User], tags=["Usuários"])
def read_users(skip: int = 0, limit: int = 100):
    return crud.get_users(skip=skip, limit=limit)

@app.get("/usuarios/{user_id}", response_model=schemas.User, tags=["Usuários"])
def read_user(user_id: int):
    db_user = crud.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/usuarios/{user_id}", response_model=schemas.User, tags=["Usuários"])
def update_user(user_id: int, user: schemas.UserUpdate):
    db_user = crud.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.senha:
        user.hash_senha()  # Hash da nova senha

    return crud.update_user(user_id, user.model_dump())

@app.delete("/usuarios/{user_id}", response_model=dict, tags=["Usuários"])
def delete_user(user_id: int):
    db_user = crud.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(user_id)
