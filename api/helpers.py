import boto3
import hashlib

def dynamodb_table(table_name):
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.Table(table_name) 
    return table

def generate_id_from_content(text_content):
    bytes_string = bytes(text_content, 'utf-8')
    return hashlib.sha256(bytes_string).hexdigest()