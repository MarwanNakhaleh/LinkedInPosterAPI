import boto3

def dynamodb_table(table_name):
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.Table(table_name) 
    return table