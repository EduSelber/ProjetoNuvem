# Documentação do Projeto para Deploy na AWS

Este documento descreve o processo de deploy de uma aplicação composta por um banco de dados PostgreSQL e uma API desenvolvida com FastAPI na AWS. Os arquivos `db-deployment.yaml` e `web-deployment.yaml` configuram os recursos necessários para o deploy usando Kubernetes.

## Arquitetura da Solução

A aplicação é composta pelos seguintes componentes:

### PostgreSQL:
- Banco de dados relacional utilizado para armazenamento de dados.
- Configurado com um Deployment e um Service.

### FastAPI:
- Aplicação web/API que interage com o banco de dados e fornece endpoints para usuários e sistemas externos.
- Configurada com um Deployment e um Service exposto como LoadBalancer para acesso externo.

## Pré-requisitos

Antes de iniciar o deploy, verifique os seguintes pré-requisitos:

### Cluster Kubernetes na AWS:
- Um cluster Kubernetes ativo configurado via Amazon EKS.

### Ferramentas Instaladas:
- **kubectl**: CLI para interagir com o cluster Kubernetes.
- **aws-cli**: CLI para gerenciamento da AWS.
- Configuração do kubectl conectada ao cluster EKS.

### Credenciais e Variáveis de Ambiente:
- Certifique-se de que as variáveis de ambiente no arquivo `web-deployment.yaml` estão configuradas corretamente (exemplo: POSTGRES_HOST, SECRET_KEY, etc.).


## Arquivos de Configuração

### 1. db-deployment.yaml

Este arquivo define o Deployment e o Service para o PostgreSQL.

#### Configuração do Deployment
- Imagem: `postgres:17`
- Variáveis de ambiente:
  - `POSTGRES_DB`: Nome do banco de dados.
  - `POSTGRES_USER`: Nome do usuário do banco.
  - `POSTGRES_PASSWORD`: Senha do banco.
- Porta exposta: 5432.

#### Configuração do Service
- Tipo: `ClusterIP` (padrão).
- Porta: 5432.

### 2. web-deployment.yaml

Este arquivo define o Deployment e o Service para a aplicação FastAPI.

#### Configuração do Deployment
- Imagem: `selber/app2:1.1`
- Variáveis de ambiente:
  - `POSTGRES_HOST`: Host do banco de dados.
  - `POSTGRES_DB`: Nome do banco.
  - `POSTGRES_USER`: Nome do usuário do banco.
  - `POSTGRES_PASSWORD`: Senha do banco.
  - Outros valores como `SECRET_KEY`, `ALGORITHM` e `ACCESS_TOKEN_EXPIRE_MINUTES`.
- Porta exposta: 8000.

#### Configuração do Service
- Tipo: `LoadBalancer`.
- Porta externa: 80.
- Porta alvo: 8000.

## Etapas para o Deploy

### 1. Criar o Banco de Dados (PostgreSQL)
Aplique o arquivo `db-deployment.yaml`:


kubectl apply -f AWS/db-deployment.yaml
### 2. Verificar se o Deployment e o Service estão ativos:
```
kubectl get deployments
```
```
kubectl get services
```

#### 2. Criar a Aplicação (FastAPI)
 Edite o arquivo web-deployment.yaml para preencher as variáveis de ambiente, como:
 POSTGRES_HOST: Nome do Service do PostgreSQL (neste caso, postgres).
 SECRET_KEY, ALGORITHM, etc.
kubectl apply -f AWS/web-deployment.yaml

### Verificar se o Deployment e o Service estão ativos:
```
kubectl get deployments
```
```
kubectl get services
```
 Anotar o endereço externo gerado pelo Service do tipo LoadBalancer:
kubectl get service fastapi-service

### 3. Acessar a Aplicação
 Usar o endereço externo do LoadBalancer para acessar a aplicação:
http://<EXTERNAL-IP>
 A API estará disponível na porta padrão 80.

### Diagnóstico e Solução de Problemas
#### Verificar Logs dos Pods:
kubectl logs <pod-name>

### Verificar Estado dos Pods:
```
kubectl get pods
```
### Testar Conexão Interna com o Banco de Dados:
 Usar o comando kubectl exec para acessar o Pod do FastAPI e testar a conexão com o banco:

```
kubectl exec -it <fastapi-pod-name> -- /bin/sh psql -h postgres -U projeto -d projeto
```

### Resolver Problemas de Endereço Externo:
 Certifique-se de que os Security Groups associados ao LoadBalancer permitem tráfego na porta 80.
 
### Códigos para Testar a Aplicação:
Nota: Altere o e-mail no payload, pois ele já foi registrado, e a aplicação não permite e-mails duplicados.
## Registro de Usuário (`/registrar/`)
```py
import requests

url = "http://a7cf1e7ce32f64a4e838214b574175f7-1913318390.us-east-1.elb.amazonaws.com/registrar/"
payload = {
  "email": "jonas2@insper.edu.br",
  "name": "Joao",
  "senha": "123456",
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.status_code)
print(response.text)
```
# Resposta do código acima:
```
200
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb25hczJAaW5zcGVyLmVkdS5iciIsImV4cCI6MTczMDMzOTg1MX0.SH5ClNEKkuHfOFf1pYBiETSdeiySKYzL-KedqK41dtk"}

```

## Login de Usuário (`/login/`)
```py
import requests

url = "http://a7cf1e7ce32f64a4e838214b574175f7-1913318390.us-east-1.elb.amazonaws.com/login/"
payload = {
  "email": "jonas2@insper.edu.br",
  "name": "Joao",
  "senha": "123456",
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.status_code)
print(response.text)

# Verifique se a resposta foi bem-sucedida e extraia o access token
if response.status_code == 200:
    data = response.json()  # Converte a resposta em formato JSON
    access_token = data.get("access_token")  # Obtém o token de acesso
    print("Access Token:", access_token)
else:
    print("Erro ao fazer login:", response.text)
```
# Resposta do código acima:
```
200
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb25hczJAaW5zcGVyLmVkdS5iciIsImV4cCI6MTczMDM0MDE4MX0.RQpgCa61NOlfCbfWjvuFZP5CwXgSCHIKpIIhteV8lIU"}
Access Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb25hczJAaW5zcGVyLmVkdS5iciIsImV4cCI6MTczMDM0MDE4MX0.RQpgCa61NOlfCbfWjvuFZP5CwXgSCHIKpIIhteV8lIU

```

## Consulta resultado da tabela do Brasileirão (`/consultar`)
```py
import requests

url = "http://a7cf1e7ce32f64a4e838214b574175f7-1913318390.us-east-1.elb.amazonaws.com/consultar"

headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)

```
# Resposta do código acima:
```
200
{"email":"jonas2@insper.edu.br","times":{"1":{"nome_time":"Botafogo","pontuacao":"64","jogos":"31","vitorias":"19","empates":"7","derrotas":"5","gols_pro":"49","gols_contra":"26","saldo_gols":"23","aproveitamento":"68"},"2":{"nome_time":"Palmeiras","pontuacao":"61","jogos":"31","vitorias":"18","empates":"7","derrotas":"6","gols_pro":"53","gols_contra":"25","saldo_gols":"28","aproveitamento":"65"},"3":{"nome_time":"Fortaleza","pontuacao":"57","jogos":"31","vitorias":"16","empates":"9","derrotas":"6","gols_pro":"41","gols_contra":"32","saldo_gols":"9","aproveitamento":"61"},"4":{"nome_time":"Flamengo","pontuacao":"55","jogos":"31","vitorias":"16","empates":"7","derrotas":"8","gols_pro":"50","gols_contra":"37","saldo_gols":"13","aproveitamento":"59"},"5":{"nome_time":"Internacional","pontuacao":"53","jogos":"31","vitorias":"14","empates":"11","derrotas":"6","gols_pro":"42","gols_contra":"28","saldo_gols":"14","aproveitamento":"56"},"6":{"nome_time":"São Paulo","pontuacao":"51","jogos":"31","vitorias":"15","empates":"6","derrotas":"10","gols_pro":"42","gols_contra":"33","saldo_gols":"9","aproveitamento":"54"},"7":{"nome_time":"Bahia","pontuacao":"46","jogos":"31","vitorias":"13","empates":"7","derrotas":"11","gols_pro":"42","gols_contra":"37","saldo_gols":"5","aproveitamento":"49"},"8":{"nome_time":"Cruzeiro","pontuacao":"44","jogos":"31","vitorias":"12","empates":"8","derrotas":"11","gols_pro":"36","gols_contra":"33","saldo_gols":"3","aproveitamento":"47"},"9":{"nome_time":"Vasco da Gama","pontuacao":"43","jogos":"31","vitorias":"12","empates":"7","derrotas":"12","gols_pro":"36","gols_contra":"43","saldo_gols":"-7","aproveitamento":"46"},"10":{"nome_time":"Atlético-MG","pontuacao":"41","jogos":"30","vitorias":"10","empates":"11","derrotas":"9","gols_pro":"42","gols_contra":"45","saldo_gols":"-3","aproveitamento":"45"},"11":{"nome_time":"Grêmio","pontuacao":"38","jogos":"31","vitorias":"11","empates":"5","derrotas":"15","gols_pro":"36","gols_contra":"39","saldo_gols":"-3","aproveitamento":"40"},"12":{"nome_time":"Criciúma","pontuacao":"37","jogos":"31","vitorias":"9","empates":"10","derrotas":"12","gols_pro":"38","gols_contra":"44","saldo_gols":"-6","aproveitamento":"39"},"17":{"nome_time":"Bragantino","pontuacao":"34","jogos":"31","vitorias":"8","empates":"10","derrotas":"13","gols_pro":"34","gols_contra":"40","saldo_gols":"-6","aproveitamento":"36"},"18":{"nome_time":"Juventude","pontuacao":"34","jogos":"31","vitorias":"8","empates":"10","derrotas":"13","gols_pro":"38","gols_contra":"48","saldo_gols":"-10","aproveitamento":"36"},"19":{"nome_time":"Cuiabá","pontuacao":"27","jogos":"31","vitorias":"6","empates":"9","derrotas":"16","gols_pro":"25","gols_contra":"41","saldo_gols":"-16","aproveitamento":"29"},"20":{"nome_time":"Atlético Goianiense","pontuacao":"22","jogos":"31","vitorias":"5","empates":"7","derrotas":"19","gols_pro":"23","gols_contra":"50","saldo_gols":"-27","aproveitamento":"23"}}}

```
### Link do vídeo:
Você pode assistir ao vídeo [aqui](https://www.youtube.com/watch?v=0TLTqTMiq_M).
