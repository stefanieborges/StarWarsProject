import boto3
import os

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")  # região correta

# Pega o nome da tabela via variável de ambiente, ou usa 'users' como fallback
users_table_name = os.getenv("USERS_TABLE_NAME", "users")

# Usa a variável corretamente aqui
users_table = dynamodb.Table(users_table_name)