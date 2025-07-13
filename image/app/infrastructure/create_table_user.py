from db import users_table, dynamodb  # ✅ importa de forma limpa, sem loops

def create_users_table():
    existing_tables = [table.name for table in dynamodb.tables.all()]
    if users_table in existing_tables:
        print(f"Tabela '{users_table}' já existe.")
        return

    table = dynamodb.create_table(
        TableName=users_table,
        KeySchema=[
            {"AttributeName": "username", "KeyType": "HASH"}
        ],
        AttributeDefinitions=[
            {"AttributeName": "username", "AttributeType": "S"}
        ],
        BillingMode="PAY_PER_REQUEST"
    )
    table.wait_until_exists()
    print(f"Tabela '{users_table}' criada com sucesso!")

create_users_table()
