import os
import logging
import json
import uuid
from base64 import b64decode

from helpers import dynamodb_table, generate_id_from_content

logging.basicConfig(format="%(asctime)s: %(levelname)s: %(message)s")
log = logging.getLogger("LinkedInPosterAPI")
log.setLevel(logging.INFO)

def get_all_categories(table):
    try:
        response = table.scan()
        categories = [x["category"] for x in response["Items"]]
        # log.info("found categories " + str(categories))
        return categories
    except Exception as e:
        log.error("Unable to get categories from table: " + e)
        return []
    
def bad_request(reason):
    return {
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Credentials": True,
            "Content-Type": "application/json"
        },
        "statusCode": 400,
        "body": json.dumps({
            "error": reason
        })
    }

def lambda_handler(event, context):
    try:
        # log.info(json.dumps(event))
        event_body = json.loads(b64decode(event["body"]))
        
        if len(event_body["content"]) < 12:
            return bad_request("You need some substance in your post.")
        
        if len(event_body["content"]) > 3000:
            return bad_request("You can only have 3000 characters in a post.")

        posts_table = dynamodb_table(os.environ["POST_TABLE"])
        categories_table = dynamodb_table(os.environ["CATEGORY_TABLE"])
        categories = get_all_categories(categories_table)
        
        if event_body["category"] in categories:
            response = posts_table.put_item(
                Item={
                    'content': event_body["content"],
                    'hasBeenPosted': "false",
                    'id': generate_id_from_content(event_body["content"]),
                    'links': event_body["links"],
                    'category': event_body["category"]
                }
            )
            
            log.info(str(response))
            
            return {
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "*",
                    "Access-Control-Allow-Credentials": True,
                    "Content-Type": "application/json"
                },
                "statusCode": 201,
                "body": str(response)
            }
        else:
            return bad_request("Choose an existing category from the following: " + str(categories))
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