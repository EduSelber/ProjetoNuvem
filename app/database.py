########## Usuários ##########
# Dicionário que simula um banco de dados de usuários, incluindo detalhes como email, nome e senha (hash)
user_db = {
    1: {
        "id": 1,
        "email": "cloud@insper.edu.br",
        "name": "Cloud",
        "senha": "$2b$12$examplehashedpassword",  # Exemplo de senha com hash bcrypt
    },
    2: {
        "id": 2,
        "email": "tifa@insper.edu.br",
        "name": "Tifa",
        "senha": "$2b$12$examplehashedpassword",  # Exemplo de senha com hash bcrypt
    },
}

########## Contador de IDs ##########
# Contador para simular auto incremento de IDs de usuários
user_id_counter = 3  # Começando do 3 para novos usuários
