from fastapi import APIRouter, HTTPException, Form, Depends
from datetime import timedelta
from app.services.auth_service import authenticate_user, create_access_token, get_current_user, pwd_context, ACCESS_TOKEN_EXPIRE_MINUTES
from app.infrastructure.db import users_table
from app.domain.enums import Role

# Router Auth

auth_router = APIRouter(tags=["Auth"])

@auth_router.post("/login", summary="Gera um token JWT após o login.")
def login(
        username: str = Form(...),
        password: str = Form(...)
):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"],
              "role": user["role"]
        },
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/register", summary="Registra um novo usuário após feita a autenticação com um token JWT de um usuário Grão-Mestre Jedi.")
def register(
    username: str = Form(...),
    password: str = Form(...),
    role: Role = Form(...),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != Role.grao_mestre_jedi:
        raise HTTPException(status_code=403, detail="Apenas um Grão-Mestre Jedi pode registrar novos usuários.")

    hashed_password = pwd_context.hash(password)
    try:
        users_table.put_item(
            Item={
                "username": username,
                "hashed_password": hashed_password,
                "role": role.value
            },
            ConditionExpression="attribute_not_exists(username)"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Usuário já existe ou erro no banco")

    return {"message": "Usuário registrado com sucesso"}