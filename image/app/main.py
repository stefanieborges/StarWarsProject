from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from mangum import Mangum
from fastapi.responses import HTMLResponse
import os
from fastapi.openapi.utils import get_openapi
from app.routes.starwars_route import starwars_router
from app.routes.auth_route import auth_router

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
        <link rel="icon" type="image/png" href="https://stefanie-starwars-img.s3.us-east-1.amazonaws.com/Star_Wars_Logo.svg.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAXXIFQRABVULKSHM7%2F20250713%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250713T083958Z&X-Amz-Expires=300&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCICkobSOIQnR8Nd647ZqQBrcPdRLL1HCPB0NVzMCQ0BDqAiEA%2FzHdX8A7tANh%2FdPk6T87Rl6xemwBee7oFdPivgnb1dcq1gIIEhAAGgw1MzA5NzY5MDExMjMiDMxQWVudGEnsDnwMZyqzAo9det9doHWvsiaabSqjdQssaidAu2qt%2FvH%2F7xnZ5yRVcLRuQlVN%2B232gG44GFAO7nLFjBFX%2BxlJ7k9327Y0IX1ExFyCU3Ebd7w1LfHbKy9tzibNym5LzD9PuW3lWSwZtcK31N%2BkDDZcw0FnM5WKOc1r4KkUf4QL3LlIzLOXGwTIITmIh1y1Tv%2BhsszaUjo6VrLDzrhJFMUpzU1YBcoorgOnxoRreDc5UBoRAA1eZ3bHRBveZiPoly1dktF6XqEO%2FRoGfa3BKtR8FgOpT%2BT%2FX9E%2BD8sq1zlcAWQsHofHeAV%2FuIYLXhOQZqeB8HWkn%2FnBIjD%2FlZAkUWL%2BMxyDoaVGD85EMe6LZRxUrEsEB27iot7EpEkCP3aKQAhGCtbS8JPgHaOUhDRjoAeKf6ULOlHuhAMG124w9ODNwwY6rQIyts6Mw%2FSnbhQtqNmm6Tma6o7k%2FEfIV8TMud0A%2FHAe0QE%2B7520BNw%2Brlb18kxVrde71odQDsy6YS%2F8SOXHlOeDEUPYba%2BAnRJDbjMWbnbHfM7ZdK5CRKsaT3mGM51gYQC4agWvSsyY7bbttuq%2FoGUvLOdxAZFdSJJWiAGDRpPnqPm0V6exblmWtDxQECYIzS8P1wm2UdCf82V0BK09n0QystH3FcRIEAC1yfa3BniLt9FRsR%2FfMbyV1lfQzDVtgEWj%2FBxK0%2BzwMEE4WA%2BqcnRy%2Bbs1mQ%2BqRjtNPBRtnivLLFXlcfPeNuLKuGUc4Cb71CHhRRXnygTQIfJS7DNNjsHtWALvHT9eNANp%2B0vOJsUREE9AiwhYypQ2z7u3dCzOLaFKOsbJsnT5UuajXlUJ&X-Amz-Signature=b580b54e25993ddd3b260f88d4c3accaeac66437f11ebaf83e76d9936a0275ce&X-Amz-SignedHeaders=host&response-content-disposition=inline">
        <style>
            * {
              box-sizing: border-box;
            }
            
            html, body {
              margin: 0;
              padding: 0;
              height: 100vh;
              overflow: hidden;
              background-color: black;
              color: yellow;
              font-family: 'Orbitron', sans-serif;
              display: flex;
              flex-direction: column;
              justify-content: center;
              align-items: center;
              text-align: center;
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
            
            .doc { background-color: #FFD700; }    
            .swagger { background-color: #00FFFF; }
            .github { background-color: #FF69B4; } 
            
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
          Com ela, você pode explorar dados da franquia galáctia como <strong>personagens</strong>, <strong>filmes</strong>, <strong>naves</strong> e <strong>planetas</strong>.<br><br>
          Comece agora a explorar esses dados… e que a força esteja com todos vocês! 
        </p>
        <div class="button-container">
          <a href="https://github.com/stefanieborges/StarWarsProject#readme" target="_blank" class="btn doc">Documentação</a>
          <a href="https://2wvq0kil3b.execute-api.us-east-1.amazonaws.com/prod/docs" target="_blank" class="btn swagger">Swagger</a>
          <a href="https://github.com/stefanieborges/StarWarsProject" target="_blank" class="btn github">GitHub</a>
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
