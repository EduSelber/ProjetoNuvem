# Usando a imagem base oficial do Python para FastAPI
FROM python:3.11-slim

# Definindo o diretório de trabalho no container
WORKDIR /app

# Copiando o arquivo de dependências para o diretório de trabalho
COPY requirements.txt .

# Instalando as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiando o código da aplicação para o container
COPY . .

# Expondo a porta da API
EXPOSE 8000

# Comando para rodar a aplicação FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
