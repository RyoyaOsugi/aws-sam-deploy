import json
import boto3
import datetime
import logging

translate = boto3.client('translate')

dynamodb = boto3.resource('dynamodb')
translate_history_table = dynamodb.Table('tranlate-history')

def lambda_handler(event, context):
    
    input_text = event['queryStringParameters']['input_text']

    try:
        response = translate.translate_text(
            Text=input_text,
            SourceLanguageCode='ja',
            TargetLanguageCode='en'
        )
    except Exception :
        # logging.error(e.response['Error']['Message'])
        # raise Exception("[ErrorMessage]: " + str(e))
        raise ExtendException(400, "Bad Request")
        
    output_text = response.get('TranslatedText')
    
    translate_history_table.put_item(
        Item = {
            'timestamp': datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
            'input_text': input_text,
            'output_text': output_text
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'output_text': output_text
        }),
        'isBase64Encoded': False,
        'headers': {}
    }

class ExtendException(Exception):
    def __init__(self, statusCode, description):
        self.statusCode = statusCode
        self.description = description

    def __str__(self):
        obj = {
            "statusCode": self.statusCode,
            "description": self.description
        }
        return json.dumps(obj)