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
# 1. Verificar se o Deployment e o Service estão ativos:
kubectl get deployments
kubectl get services


# 2. Criar a Aplicação (FastAPI)
# Edite o arquivo web-deployment.yaml para preencher as variáveis de ambiente, como:
# POSTGRES_HOST: Nome do Service do PostgreSQL (neste caso, postgres).
# SECRET_KEY, ALGORITHM, etc.
kubectl apply -f AWS/web-deployment.yaml

# Verificar se o Deployment e o Service estão ativos:
kubectl get deployments
kubectl get services

# Anotar o endereço externo gerado pelo Service do tipo LoadBalancer:
kubectl get service fastapi-service

# 3. Acessar a Aplicação
# Usar o endereço externo do LoadBalancer para acessar a aplicação:
# http://<EXTERNAL-IP>
# A API estará disponível na porta padrão 80.

# Diagnóstico e Solução de Problemas
# Verificar Logs dos Pods:
kubectl logs <pod-name>

# Verificar Estado dos Pods:
kubectl get pods

# Testar Conexão Interna com o Banco de Dados:
# Usar o comando kubectl exec para acessar o Pod do FastAPI e testar a conexão com o banco:
kubectl exec -it <fastapi-pod-name> -- /bin/sh
psql -h postgres -U projeto -d projeto

# Resolver Problemas de Endereço Externo:
# Certifique-se de que os Security Groups associados ao LoadBalancer permitem tráfego na porta 80.
