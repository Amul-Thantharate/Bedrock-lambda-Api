import json
import boto3
import botocore
from datetime import datetime
import base64
import botocore.config
import pytz
# If function succed then publish message to SNS topic else email to image generated

def publish_to_sns(summary, topic_arn):
    sns = boto3.client('sns')
    try:
        sns.publish(
            TopicArn=topic_arn,
            Message=summary
        )
        print("Summary published to SNS")
    except Exception as e:
        print("Error when publishing summary to SNS")
        return ""    

def lambda_handler(event, context):

    event = json.loads(event['body'])
    message = event['message']

    bedrock = boto3.client("bedrock-runtime",region_name="us-east-1",config = botocore.config.Config(read_timeout=300, retries = {'max_attempts':3}))

    s3 = boto3.client('s3')

    payload = {
        "text_prompts":[{f"text":message}],
        "cfg_scale":10,
        "seed":0,
        "steps":100
    }

    response = bedrock.invoke_model(body=json.dumps(payload),modelId = 'stability.stable-diffusion-xl-v0',contentType = "application/json",accept = "application/json")

    response_body = json.loads(response.get("body").read())
    base_64_img_str = response_body["artifacts"][0].get("base64")
    image_content = base64.decodebytes(bytes(base_64_img_str,"utf-8"))
    bucket_name = 'bedrock-meeting-summarization'
    utc_now = datetime.now(pytz.utc)
    current_time = utc_now.astimezone(pytz.timezone('Asia/Kolkata')).strftime('%H%M%S')
    s3_key = f"output-images/{current_time}.png"
    s3.put_object(Bucket = bucket_name, Key = s3_key, Body = image_content, ContentType = 'image/png')
    print("Image saved to s3")
    topic_arn = "Add your SNS topic arn here" # Add your SNS topic arn here
    publish_to_sns(s3_key, topic_arn)


    return {
        'statusCode': 200,
        'body': json.dumps('Image Saved to s3')
    }
