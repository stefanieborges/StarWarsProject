from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from mangum import Mangum
from fastapi.responses import HTMLResponse
import os
from fastapi.openapi.utils import get_openapi
from app.controllers.starwars_controller import starwars_router
from app.controllers.auth_controller import auth_router

IS_AWS = os.environ.get("IS_AWS", "").lower() == "true"

app = FastAPI(
    title="🌌 StarWars API",
    version="1.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
    description=
"""
✨ **Bem-vindo à Star Wars API!** ✨  
Explore os dados mais épicos da galáxia!

---

🧑‍💻 **Como usar:**

1. Faça o primeiro login em `/login` com:
   - `username`: `yoda`  
   - `password`: `jedi123`  

   Este é o **Grão-Mestre Jedi** da API (usuário com role `admin`).  
   Ele possui acesso total e pode cadastrar novos usuários com os seguintes perfis:
   - **Padawan**: acesso apenas ao endpoint `/starwars`
   - **Grão-Mestre Jedi**: acesso aos endpoints `/starwars` e `/register`

2. Copie o **token JWT** gerado após o login.

3. Clique em **Authorize 🔒** (canto superior da documentação Swagger) e cole o token.  
   ⚠️ **Não é necessário escrever `Bearer` antes do token.**

4. Acesse o endpoint `/starwars` para realizar buscas.

---

👽 **Exemplo de uso com a categoria `people`:**

Você pode consultar dados de 4 maneiras:

- ✅ **Sem parâmetros**: retorna todos os registros da categoria.
- 🔍 **Com o parâmetro `people` preenchido**: retorna o personagem exato digitado.
- 🧠 **com parâmetros correlacionados** à categoria. Exemplo:\n
    * Pesquisar **Millennium Falcon** nessa categoria retornaria **(Chewbacca, Han Solo, Lando Calrissian e Nien Nunb)** que já foram os portadores dessa nave.
- ⚙️ **Com filtros ordenados** de forma crescente(asc) e decrescente(desc), como `gender`, `birth_year`, etc.
"""
,
    root_path="/prod" if IS_AWS else ""
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", include_in_schema=False)
def homepage():
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
      <head>
        <title>Star Wars API</title>
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400..900&family=Press+Start+2P&display=swap" rel="stylesheet">
        <link rel="icon" type="image/png" href="https://stefanie-starwars-img.s3.us-east-1.amazonaws.com/Star_Wars_Logo.svg.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAXXIFQRABXFLHVER3%2F20250713%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250713T010109Z&X-Amz-Expires=300&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPH%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIQCH60b6k1vu%2Butd8QitY4UDpggJBrZZmIYsicrieUIQAgIgfKwUy8XDXGWToW2cii6Kxq7t304ilzltjXvZAI7mEVUq4AII%2Bv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw1MzA5NzY5MDExMjMiDC4uYmqy7jrTeP%2ByuCq0Ar3IdwRHrxfaVaWT3iBWoiRN9s0URDiRAMHg3C98zJ8FhWiGBmWYIaUMrIjob4u1FdIRLEhPCyoeY1eb6Honpefkv1vllicaW2Gy%2F%2BjvxmDmSAEa0Vz%2FAhjJUulnAdjRtIxuj2YyIIF7VXYrxG0i3dBGjW4ZNpMvndz8PjQgY%2BpVUu2rd0d%2FB3rDBpgfjKj9N2GgGNRemZcqhO8KaARXGO3hiSzl%2Fidjc1o%2BmzU%2BoQVqm0uo%2FXT9yTa3P28L%2B4fC9avbqT4cU75FdNziEK8huVEjT3cUNHaeO8LW0m197Ok%2FWcWE9SfBrpQRieQHjW0k8%2BppPNSptvl3yhG09MtfKo27HIMcVEBnqSL9jIzG2GVHlnJKr4PHHdP6%2B6hMGeFBqUBxYQ2aqWd6t7M6We43LOkXckQZMKXXysMGOq0CIgJi8Z7wjSFbgRehZ511WmI5YX%2BVdAIEDTL8%2B78nsdmfdTthJ5lhKWNUVa0b6LWmSod4E8LNIQ8uLW5OtkPrpKJ8TYMOJhZQfH4D4Ec8GLKcK0PUzPNAYpbEMc6XNhR5AzSqkzGKp2ExNb3p52dAnJxWeAIZTKrGvOJUCn9FsPvNv3HlDkeVUdLmTvqiU153d69CAtrHbCHKczTxs6iCy73N1Z7kxhoTpH8kaenFiSyp%2FvfEOAxO3klxx9kq%2FX18Yc%2FpaFnRNkMcHDMARZpgu%2B%2ByK%2FEf9%2BfdBMhIGbq3Ayzm4GjRVYawJKyBBCkSTeoXIOIx6cKd8BexNWBI%2Fp8kI2VSKQCMknDzIlJPpTBEBLVaXaOdZV%2BdKu0ppcaU2gOZZEE57VJME1eUEVNiQg%3D%3D&X-Amz-Signature=826c026ca1eeb8ed08a28424b861b800fe84d59b921e80967bae23bcbde4a759&X-Amz-SignedHeaders=host&response-content-disposition=inline">
        <style>
          body {
            background-color: black;
            color: yellow;
            font-family: 'Orbitron', sans-serif;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            text-align: center;
            padding: 20px;
          }

          h1 {
            font-family: 'Press Start 2P', cursive;
            font-size: 2.2em;
            margin-bottom: 20px;
            animation: fadein 4s ease-in-out;
            color: yellow;
            text-shadow: 2px 2px 5px #FFD700;
          }

          p {
            font-family: 'Orbitron', sans-serif;
            font-size: 1rem;
            color: white;
            max-width: 800px;
            line-height: 1.6rem;
            animation: fadein 6s ease-in-out;
            margin-bottom: 30px;
          }

          .button-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            animation: fadein 7s ease-in-out;
          }

          .btn {
            font-family: 'Press Start 2P', cursive;
            font-size: 0.8rem;
            padding: 15px 25px;
            border: none;
            border-radius: 10px;
            text-decoration: none;
            color: black;
            cursor: pointer;
            box-shadow: 0 0 10px white;
            transition: transform 0.3s ease-in-out;
          }

          .btn:hover {
            transform: scale(1.1);
          }

          /* Cores aleatórias */
          .doc { background-color: #FFD700; }     /* dourado */
          .swagger { background-color: #00FFFF; } /* ciano */
          .github { background-color: #FF69B4; }  /* rosa */

          @keyframes fadein {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
          }
        </style>
      </head>
      <body>
        <h1>StarWars API</h1>
        <p>
          Bem-vindo à minha API desenvolvida para o processo seletivo da <strong>PowerOfData</strong>!<br><br>
          Com ela, você pode explorar dados da galáxia como <strong>personagens</strong>, <strong>filmes</strong>, <strong>naves</strong> e <strong>planetas</strong>.<br><br>
          A aplicação utiliza <strong>Python</strong>, <strong>FastAPI</strong>, <strong>AWS Lambda</strong>, <strong>API Gateway</strong> e <strong>DynamoDB</strong>.<br><br>
          Comece agora a explorar esses dados… e que a força esteja com todos vocês! 
        </p>
        <div class="button-container">
          <a href="https://github.com/stefanieborges/StarWarsAPI#readme" target="_blank" class="btn doc">Documentação</a>
          <a href="https://2wvq0kil3b.execute-api.us-east-1.amazonaws.com/prod/docs" target="_blank" class="btn swagger">Swagger</a>
          <a href="https://github.com/stefanieborges/StarWarsAPI" target="_blank" class="btn github">GitHub</a>
        </div>
      </body>
    </html>
    """)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"HTTPBearer": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
app.include_router(auth_router)
app.include_router(starwars_router)

if IS_AWS:
    handler = Mangum(app)
