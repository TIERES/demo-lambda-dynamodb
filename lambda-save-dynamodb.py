# CloudFaster Academy: Demo de aplicação que recebe dados enviados via Api Gateway e grava no DynamoDB
# Pré-requisitos: 
# 1) Tabela do DynamoDB
# 2) IAM Role com permissão de escrita/leitura na tabela do DynamoDB

import json
from uuid import uuid4
import boto3 #AWS SDK para Python3
from boto3.dynamodb.types import TypeSerializer

# substitua essa variavel com o nome da tabela criada no DynamoDB
DYNAMODB_TABLE = "lab-dynamodb"
# subistitua essa variavel com a região da AWS onde sua tabela do DynamoDB foi criada
AWS_REGION = "us-east-1"

def putItemDynamoDB(table, item):
    """Função que adiciona um novo item a uma tabela do DynamoDB

    Parâmetros:
        table: str [Obrigatório] Tabela onde o item será armazenado
        item: dict [Obrigatório] Item no formato JSON
    """
    try:
        dynamo = boto3.client('dynamodb', region_name=AWS_REGION)
        s = TypeSerializer()
        r = dynamo.put_item(
            TableName=table,
            Item={k: s.serialize(v) for k, v in item.items() if v != ""}
        )
        print("Resultado do PUT ITEM:")
        print(r)
        return { "success": True, "message": "Dados gravados com sucesso.", "data": { "id": item['id'] } }
    except Exception as err:
        print("Falha ao gravar no DynamoDB")
        print("Tabela: ", table)
        print("Item: ", item)
        print("Regiao: ", AWS_REGION)
        print(err)
        return { "success": False, "message": err, "data": {} }

def lambda_handler(event, context):
    """Função principal da aplicação, essa função deve ser informada como a "handler" do Lambda

    Parâmetros: 
        event: dict - Contém os dados do evento que foi o acionador do Lambda
        context: dict - Contém os dados do contexto da requisição, dados do ambiente, id da requisição, etc...
    """
    # funcao principal da aplicação, responsável por receber os dados do evento e contexto da requisição
    print("Dados do evento recebido:")
    print(event)
    print("Dados do contexto recebido:")
    print(context)
    # verifica os campos que iremos gravar na tabela foram informados e adiciona a um dicionario que será gravado no DynamoDB
    data = {
        "id": str(uuid4()),
        "nome": event['nome'] if "nome" in event and event['nome'] else None,
        "idade": event['idade'] if "idade" in event and event['idade'] else None,
        "jogo": event['jogo'] if "jogo" in event and event['jogo'] else None,
        "pontuacao": event['pontuacao'] if "pontuacao" in event and event['pontuacao'] else None
    }
    # como nosso único campo obrigatório é o nome verifica se foi informado
    if data['nome'] != None:
        # campo nome informado, grava os dados na tabela do DynamoDB e retorna o resultado
        return putItemDynamoDB(DYNAMODB_TABLE, data)
    else:
        # se o nome não foi informado retorna uma mensagem de erro
        return {
            "success": False,
            "message": "Campo Nome não foi informado."
        }