import boto3
import json
import urllib.parse
from datetime import datetime

# Initialize AWS clients
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PetsPedidos')
sns = boto3.client('sns')

def lambda_handler(event, context):
    # 1. Get S3 object information
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        # 2. Use Rekognition to detect pet characteristics
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
        
        # 3. Extract relevant information
        labels = [label['Name'] for label in response['Labels']]
        is_dog = 'Dog' in labels
        is_cat = 'Cat' in labels
        
        if not (is_dog or is_cat):
            return {
                'statusCode': 200,
                'body': json.dumps('Image does not contain a recognizable pet')
            }
        
        # 4. Identify breed (if available) - expanded breed list
        common_breeds = ['Labrador Retriever', 'Golden Retriever', 'Siamese', 
                        'German Shepherd', 'Bulldog', 'Beagle', 'Poodle',
                        'Persian', 'Maine Coon', 'Bengal']
        breed = next(
            (label['Name'] for label in response['Labels'] 
             if label['Name'] in common_breeds),
            'Unknown'
        )
        
        # 5. Detect additional attributes
        face_response = rekognition.detect_faces(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key
                }
            },
            Attributes=['ALL']
        )
        
        age_range = None
        if face_response.get('FaceDetails'):
            age_range = face_response['FaceDetails'][0].get('AgeRange', {})
        
        # 6. Prepare DynamoDB item
        item = {
            'PetID': key.split('.')[0],  # Use filename as ID
            'ImagemURL': f"https://{bucket}.s3.amazonaws.com/{key}",
            'Raca': breed,
            'Tipo': 'Dog' if is_dog else 'Cat',
            'Caracteristicas': labels,
            'DataProcessamento': datetime.now().isoformat(),
            'Status': 'Processado',
            'AgeRange': age_range
        }
        
        # 7. Store in DynamoDB
        table.put_item(Item=item)
        
        # 8. Send SNS notification
        sns.publish(
            TopicArn='arn:aws:sns:REGION:ACCOUNT_ID:TOPIC_NAME',
            Message=json.dumps(item),
            Subject='Novo Pet Processado'
        )
        
        # 9. Log and return
        print(f"Pet processed: {item}")
        return {
            'statusCode': 200,
            'body': json.dumps('Processing completed successfully!')
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing image')
        }
