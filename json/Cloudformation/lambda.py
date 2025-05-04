import boto3
import json
import urllib.parse
from datetime import datetime

# Inicializa clientes AWS
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PetsPedidos')  # Nome da tabela DynamoDB

def lambda_handler(event, context):
    # 1. Obtém informações do objeto S3 que disparou o evento
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        # 2. Usa Rekognition para detectar características do pet
        response = rekognition.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key
                }
            },
            MaxLabels=10,
            MinConfidence=70
        )
        
        # 3. Extrai informações relevantes
        labels = [label['Name'] for label in response['Labels']]
        is_dog = 'Dog' in labels
        is_cat = 'Cat' in labels
        
        if not (is_dog or is_cat):
            return {
                'statusCode': 200,
                'body': json.dumps('Imagem não contém um pet reconhecível')
            }
        
        # 4. Identifica raça (se disponível)
        breed = next(
            (label['Name'] for label in response['Labels'] 
            if label['Name'] in ['Labrador', 'Golden Retriever', 'Siamese']  # Exemplo de raças
        ), 'Desconhecida')
        
        # 5. Armazena no DynamoDB
        item = {
            'PetID': key.split('.')[0],  # Usa o nome do arquivo como ID
            'ImagemURL': f"https://{bucket}.s3.amazonaws.com/{key}",
            'Raca': breed,
            'Tipo': 'Cachorro' if is_dog else 'Gato',
            'Caracteristicas': labels,
            'DataProcessamento': datetime.now().isoformat(),
            'Status': 'Processado'
        }
        
        table.put_item(Item=item)
        
        # 6. Log e retorno
        print(f"Pet processado: {item}")
        return {
            'statusCode': 200,
            'body': json.dumps('Processamento concluído com sucesso!')
        }
        
    except Exception as e:
        print(f"Erro: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Erro no processamento da imagem')
        }
    
    sns = boto3.client('sns')
    sns.publish(
        TopicArn='arn:aws:sns:REGION:ACCOUNT_ID:TOPIC_NAME',  # Substitua pelos valores corretos
        Message=f"json.dumps(item)",
        Subject='Novo Pet Processado'
    )

    location = rekognition.detect_faces(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        Attributes=['ALL']
    )

    location = boto3.client('location')
    location.put_item(
        TableName='PetsPedidos',
        Item={
            'PetID': key.split('.')[0],
            'Location': {
                'Latitude': location['FaceDetails'][0]['BoundingBox']['Left'],
                'Longitude': location['FaceDetails'][0]['BoundingBox']['Top']
            }
        }
    )
