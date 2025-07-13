# StarWars API

API criada usando, principalmente:

- Python
- FastAPI  
- Swagger  
- AWS Lambda  
- API Gateway  
- DynamoDB  
- CloudWatch  
- AWS CLI  
- AWS CDK  
- Docker  
- JWT  
- Clean Architecture
- Pytest
- Github Actions

## Estrutura do projeto 
Seguindo os princípios de Clean Architecture:

<img src="https://github.com/stefanieborges/StarWarsProject/blob/master/githubImg/EstruturaProjeto.png"/>

## Integração com o DynamoDB

Para registrar novos usuários e testar os níveis de acessos dinamicamente, foi necessário utilizar um banco de dados.

Ao rodar aws dynamodb scan --table-name users --region us-east-1 é possível ter o retorno de todos os usuários registrados, suas senhas em formato hash usando o bcrypt e seus roles.

<img src="https://github.com/stefanieborges/StarWarsProject/blob/master/githubImg/SaidaTabelaUsers.png"/>

## Deploy
Após os ajustes de configuração da conta foi feito o deploy usando uma imagem do docker e AWS CDK.

## Após o deploy - CloudWatch

Os logs da API ao irem para a produção puderam ser observados através desa ferramenta de monitoramento e os devidos ajustes foram feitos a medida dos erros apontados nessa plataforma.

## Github Actions e Pytest
Foram feitos teste tanto em ambient Linux e Windows. Acesse o <a href="https://github.com/stefanieborges/StarWarsProject/actions/runs/16248864919">Actions</a>.

## Como usar a api

1- Faça o primeiro login no endpoint /login com:

username: yoda

password: jedi123

Este é o Grão-Mestre Jedi da API (usuário com role master).
Ele possui acesso total e pode cadastrar novos usuários com os seguintes perfis:

- Padawan: acesso apenas ao endpoint /starwars
- Grão-Mestre Jedi: acesso aos endpoints /starwars e /register

2 - Copie o token JWT gerado após o login.

3 - Clique em Authorize 🔒 (canto superior da documentação Swagger) e cole o token.
⚠️ Não é necessário escrever Bearer antes do token.

4 - Acesse o endpoint /starwars para realizar buscas.

👽 Exemplo de uso com a categoria people:

Você pode consultar dados de 4 maneiras:

- ✅ Sem parâmetros: retorna todos os registros da categoria.

- 🔍 Com o parâmetro people preenchido: retorna o personagem exato digitado.

- 🧠 com parâmetros correlacionados à categoria. 

Exemplo:

Pesquisar Millennium Falcon nessa categoria retornaria (Chewbacca, Han Solo, Lando Calrissian e Nien Nunb) que já foram os portadores dessa nave.
⚙️ Com filtros ordenados de forma crescente(asc) e decrescente(desc), como gender, birth_year, etc.
