import requests
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt  # Importar para trabalhar com JWT
from datetime import timedelta, datetime
import crud
import schemas
import bcrypt  # Import necessário para verificar a senha
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

app = FastAPI()

# Configurações do JWT
SECRET_KEY = "seu_segredo_aqui"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Definir o esquema OAuth2 para o token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para verificar o token de acesso
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/registrar/", response_model=dict, tags=["Usuários"])
def create_user(user: schemas.UserCreate):
    db_user = crud.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="User already registered")

    user.hash_senha()  # Hash da senha antes de salvar
    new_user = crud.create_user(user.model_dump())

    # Gerar JWT token após o registro
    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token}  # Retorna apenas o token

@app.post("/login/", response_model=dict, tags=["Usuários"])
def login_user(user: schemas.UserCreate):
    db_user = crud.get_user_by_email(user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verificar se a senha fornecida corresponde ao hash armazenado
    if not bcrypt.checkpw(user.senha.encode('utf-8'), db_user["senha"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    # Gerar o token JWT após o login bem-sucedido
    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token}

@app.get("/me", response_model=dict, tags=["Usuários"])
def read_current_user(token: str = Depends(oauth2_scheme)):
    # Verificar a validade do token
    email = verify_access_token(token)

    # Buscar usuário no banco de dados com base no email recuperado do token
    db_user = crud.get_user_by_email(email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # URL para scraping
    url = "https://www.terra.com.br/esportes/futebol/brasileiro-serie-a/tabela/"
    response = requests.get(url)

    # Cria o objeto BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Dicionário para armazenar os times
    times = {}

    # Função para extrair informações das linhas
    def extrair_informacoes(linhas):
        for linha in linhas:
            colunas = linha.find_all('td')
            
            if len(colunas) > 1:  # Verifica se há colunas suficientes
                # Obtém as informações
                posicao = colunas[0].get_text(strip=True)  
                nome_time = colunas[2].get_text(strip=True)[:-2]  
                pontuacao = colunas[4].get_text(strip=True)     
                jogos = colunas[5].get_text(strip=True)  
                vitorias = colunas[6].get_text(strip=True)
                empates = colunas[7].get_text(strip=True)
                derrotas = colunas[8].get_text(strip=True)
                gols_pro = colunas[9].get_text(strip=True)
                gols_contra = colunas[10].get_text(strip=True)
                saldo_gols = colunas[11].get_text(strip=True)
                aproveitamento = colunas[12].get_text(strip=True)
                
                # Armazena as informações em um dicionário
                times[posicao] = {
                    'nome_time': nome_time,
                    'pontuacao': pontuacao,
                    'jogos': jogos,
                    'vitorias': vitorias,
                    'empates': empates,
                    'derrotas': derrotas,
                    'gols_pro': gols_pro,
                    'gols_contra': gols_contra,
                    'saldo_gols': saldo_gols,
                    'aproveitamento': aproveitamento
                }
    
    # Extrai informações das linhas de cada zona
    for zone in ['zone-1', 'zone-2', 'zone-3', 'zone-4']:
        linhas = soup.find_all('tr', class_=zone)
        extrair_informacoes(linhas)

    # Retorna o email do usuário e as informações dos times
    return {"email": email, "times": times} 