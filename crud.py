import bcrypt
from database import *

# Retorna o usuário pelo ID
def get_user(user_id: int):
    if user_id not in user_db:
        raise ValueError("User not found")
    return user_db[user_id]

# Retorna o usuário pelo email
def get_user_by_email(email: str):
    for user in user_db.values():
        if user["email"] == email:
            return user
    return None

# Retorna os 100 primeiros usuários armazenados
def get_users(skip: int = 0, limit: int = 100):
    return list(user_db.values())[skip : skip + limit]

################################################################ CREATE ################################################################

# Cria um novo usuário e adiciona no banco
def create_user(user: dict):
    global user_id_counter
    new_user = {
        "id": user_id_counter,
        "email": user["email"],
        "name": user["name"],
        "senha": user["senha"],  # Senha já está com hash
    }
    user_db[user_id_counter] = new_user
    user_id_counter += 1
    return new_user

################################################################ UPDATE ################################################################

# Atualiza os dados de um usuário existente
def update_user(user_id: int, user: dict):
    if user_id not in user_db:
        raise ValueError("User not found")

    for key, value in user.items():
        if value is not None:
            user_db[user_id][key] = value

    return user_db[user_id]

################################################################ DELETE ################################################################

# Deleta um usuário existente
def delete_user(user_id: int):
    if user_id not in user_db:
        raise ValueError("User not found")
    
    del user_db[user_id]
    return {"message": "User deleted successfully"}