# Bem-vindo à Documentação da API
## Nome: Eduardo Selber Castanho
## Visão Geral
Esta API fornece um sistema completo de gerenciamento de usuários com autenticação baseada em JWT, além de recursos adicionais, como scraping de dados de futebol ao vivo. Abaixo está um resumo das principais funcionalidades e como utilizá-las.
## Como executar:
Para executar a API, é necessário copiar o arquivo compose.yaml para o diretório do projeto e, em seguida, no terminal desse diretório, executar o comando:
```
docker compose up --build
```
. Após alguns instantes, será possível acessar `http://localhost:8000/docs`, indicando que a API está pronta para uso.
## Principais Funcionalidades
### Registro de Usuário (`/registrar/`)
- Permite que novos usuários se registrem fornecendo seu e-mail, nome e senha.
- O sistema automaticamente faz o hash da senha antes de salvá-la no banco de dados para segurança.
- Após o registro bem-sucedido, a API gera um JWT (JSON Web Token) que pode ser usado para autenticação em chamadas subsequentes.
### Login de Usuário (`/login/`)
- Permite que usuários registrados façam login usando seu e-mail e senha.
- Verifica se a senha fornecida corresponde ao hash armazenado.
- Gera um JWT após um login bem-sucedido, que pode ser usado para autenticação.
### Consulta resultado da tabela do Brasileirão (`/consultar`)
- Permite que o usuário autenticado consulte o resultado atualizado da tabela do Campeonato Brasileiro.
- Realiza a verificação da validade do token JWT fornecido no cabeçalho da requisição.
- Retorna o e-mail do usuário e as informações mais recentes sobre a tabela do campeonato brasileiro de futebol, extraídas via scraping.
### Scraping de Dados de Futebol
- A API realiza scraping da tabela ao vivo do Campeonato Brasileiro.
- Extrai informações como posição, nome do time, pontuação, jogos, vitórias, empates, derrotas, gols pró, gols contra, saldo de gols e aproveitamento.
- Retorna apenas os times das zonas 1, 2, 3 e 4, excluindo times entre as zonas 3 e 4.
- As informações extraídas são enviadas junto com o e-mail do usuário na rota /consultar.
### Códigos para Testar a Aplicação:
## Registro de Usuário (`/registrar/`)
```py
import requests

url = "http://localhost:8000/registrar/"
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
# Resposta para o código acima:
```
200
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb25hczJAaW5zcGVyLmVkdS5iciIsImV4cCI6MTczMDMzOTg1MX0.SH5ClNEKkuHfOFf1pYBiETSdeiySKYzL-KedqK41dtk"}

```

## Login de Usuário (`/login/`)
```py
import requests

url = "http://localhost:8000/login/"
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
# Resposta para o código acima:
```
200
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb25hczJAaW5zcGVyLmVkdS5iciIsImV4cCI6MTczMDM0MDE4MX0.RQpgCa61NOlfCbfWjvuFZP5CwXgSCHIKpIIhteV8lIU"}
Access Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb25hczJAaW5zcGVyLmVkdS5iciIsImV4cCI6MTczMDM0MDE4MX0.RQpgCa61NOlfCbfWjvuFZP5CwXgSCHIKpIIhteV8lIU

```

## Consulta resultado da tabela do Brasileirão (`/consultar`)
```py
import requests

url = "http://localhost:8000/consultar"

headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)

```
# Resposta para o código acima:
```
200
{"email":"jonas2@insper.edu.br","times":{"1":{"nome_time":"Botafogo","pontuacao":"64","jogos":"31","vitorias":"19","empates":"7","derrotas":"5","gols_pro":"49","gols_contra":"26","saldo_gols":"23","aproveitamento":"68"},"2":{"nome_time":"Palmeiras","pontuacao":"61","jogos":"31","vitorias":"18","empates":"7","derrotas":"6","gols_pro":"53","gols_contra":"25","saldo_gols":"28","aproveitamento":"65"},"3":{"nome_time":"Fortaleza","pontuacao":"57","jogos":"31","vitorias":"16","empates":"9","derrotas":"6","gols_pro":"41","gols_contra":"32","saldo_gols":"9","aproveitamento":"61"},"4":{"nome_time":"Flamengo","pontuacao":"55","jogos":"31","vitorias":"16","empates":"7","derrotas":"8","gols_pro":"50","gols_contra":"37","saldo_gols":"13","aproveitamento":"59"},"5":{"nome_time":"Internacional","pontuacao":"53","jogos":"31","vitorias":"14","empates":"11","derrotas":"6","gols_pro":"42","gols_contra":"28","saldo_gols":"14","aproveitamento":"56"},"6":{"nome_time":"São Paulo","pontuacao":"51","jogos":"31","vitorias":"15","empates":"6","derrotas":"10","gols_pro":"42","gols_contra":"33","saldo_gols":"9","aproveitamento":"54"},"7":{"nome_time":"Bahia","pontuacao":"46","jogos":"31","vitorias":"13","empates":"7","derrotas":"11","gols_pro":"42","gols_contra":"37","saldo_gols":"5","aproveitamento":"49"},"8":{"nome_time":"Cruzeiro","pontuacao":"44","jogos":"31","vitorias":"12","empates":"8","derrotas":"11","gols_pro":"36","gols_contra":"33","saldo_gols":"3","aproveitamento":"47"},"9":{"nome_time":"Vasco da Gama","pontuacao":"43","jogos":"31","vitorias":"12","empates":"7","derrotas":"12","gols_pro":"36","gols_contra":"43","saldo_gols":"-7","aproveitamento":"46"},"10":{"nome_time":"Atlético-MG","pontuacao":"41","jogos":"30","vitorias":"10","empates":"11","derrotas":"9","gols_pro":"42","gols_contra":"45","saldo_gols":"-3","aproveitamento":"45"},"11":{"nome_time":"Grêmio","pontuacao":"38","jogos":"31","vitorias":"11","empates":"5","derrotas":"15","gols_pro":"36","gols_contra":"39","saldo_gols":"-3","aproveitamento":"40"},"12":{"nome_time":"Criciúma","pontuacao":"37","jogos":"31","vitorias":"9","empates":"10","derrotas":"12","gols_pro":"38","gols_contra":"44","saldo_gols":"-6","aproveitamento":"39"},"17":{"nome_time":"Bragantino","pontuacao":"34","jogos":"31","vitorias":"8","empates":"10","derrotas":"13","gols_pro":"34","gols_contra":"40","saldo_gols":"-6","aproveitamento":"36"},"18":{"nome_time":"Juventude","pontuacao":"34","jogos":"31","vitorias":"8","empates":"10","derrotas":"13","gols_pro":"38","gols_contra":"48","saldo_gols":"-10","aproveitamento":"36"},"19":{"nome_time":"Cuiabá","pontuacao":"27","jogos":"31","vitorias":"6","empates":"9","derrotas":"16","gols_pro":"25","gols_contra":"41","saldo_gols":"-16","aproveitamento":"29"},"20":{"nome_time":"Atlético Goianiense","pontuacao":"22","jogos":"31","vitorias":"5","empates":"7","derrotas":"19","gols_pro":"23","gols_contra":"50","saldo_gols":"-27","aproveitamento":"23"}}}

```
## Link do vídeo:
https://youtu.be/h3qdxoTj_fM

## Autenticação
A autenticação é feita por meio de tokens JWT. Os tokens devem ser incluídos no cabeçalho das solicitações para acessar rotas protegidas.
### Exemplo de Uso
1. **Registrar um novo usuário**: Envie uma solicitação POST para `/registrar/` com o e-mail e a senha.
2. **Fazer login**: Envie uma solicitação POST para `/login/` com as credenciais do usuário.
3. **Recuperar informações do usuário**: Envie uma solicitação GET para `/consultar`, incluindo o token JWT no cabeçalho.
## Conclusão
Esta API fornece uma solução segura e eficaz para gerenciamento de usuários e acesso a dados de futebol em tempo real. Sinta-se à vontade para explorar as rotas e integrar a API em seus projetos!