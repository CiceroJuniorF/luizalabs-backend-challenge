# luizalabs-backend-challenge

# Requisitos
makefile
docker
docker-compose
python
pip


# Passo 1: Instalação de bibliotecas
Para realizar as instalações das bibliotecas execute:
`make install`

# Passo 2: Iniciando a api
Para iniciar a api rode:
`make start`
Irá rodar o docker-compose e logo em seguida irá rodar a api

# Passo 3: Acessando a doc
[Swagger](http://localhost:8000/docs)
[Redoc](http://localhost:8000/redoc)

# Passo 4: Se autenticando utilizando o fluxo Oauth2 Client Credentials
### Client Credentials é um fluxo para autenticação entre máquinas
Usuário fixo
*Usuario fixo:*
**client_id**
`luizalabs`
**client_secret**
`2d217d9b58e59fb6f3e2ad82e52c3ffe98da318b19594708fd9ed0528f3eb73a`
![alt](./img/authorize.png)
![alt](./img/authorize2.png)

# Passo 5: Utilizando a api
Após autenticado você poderá utilizar todos endpoints
---
Fluxo simples de uso: 

1 - /api/customer/create
2 - /api/customer/{customer_id}/favorite/product/add/{product_id}

Você precisa pegar o id do customer criado no passo 1 e colocar no passo 2
No passo 2 você pode utilizar os seguintes id de produtos que foram mocados para adicionar na lista do cliente:
51150cf9-2f86-4bc9-bd71-4cfccca5d111
85aafccb-44bf-4bff-b66c-f9581eb96742
8a9a59b9-5c8e-4dc4-8260-ac4a3699bccc

---
# Code

## Clean Arch
Foi utilizado um design básico de clean arch

## Chaves no arquivo .env e docker-compose.yml
Deixei as chaves configuradas apenas para ambiente local, em uma publicação, deve-se setar as seguintes váriaveis de ambiente:
SECURITY_OAUTH2_JWT_SECRET="xx"
SECURITY_OAUTH2_ACCESS_TOKEN_EXPIRE_MINUTES=30
SECURITY_OAUTH2_JWT_ALGORITHM="HS256"
CLIENT_ID="xx"
CLIENT_SECRET="xx"
USE_IN_MEMORY=0
MONGODB_URL="xx"
MONGODB_USERNAME="xx"
MONGODB_PASSWORD="xx"
MONGODB_DB="xx"

*Sobre pass encontrados nas configurações: São apenas referente ao ambiente local* 
