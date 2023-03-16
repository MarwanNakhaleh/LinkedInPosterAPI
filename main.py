import os
import logging
import json
from base64 import b64decode

from helpers import dynamodb_table

logging.basicConfig(format="%(asctime)s: %(levelname)s: %(message)s")
log = logging.getLogger("LinkedInPosterAPI")
log.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        log.info(json.dumps(event))
        event_body = json.loads(b64decode(event["body"]))

        posts_table = dynamodb_table(os.environ["POST_TABLE"])
        categories_table = dynamodb_table(os.environ["CATEGORY_TABLE"])
        
        return {
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Credentials": True,
                "Content-Type": "application/json"
            },
            "statusCode": 201,
            "body": "dookie"
        }
    except Exception as e:
        log.error(str(e))
        return {
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Credentials": True,
                "Content-Type": "application/json"
            },
            "statusCode": 500,
            "body": str(e)
        }
   
if __name__ == "__main__":
    pass