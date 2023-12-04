### Serverless Bedtime Storyteller ### 

## Description On Project 

* This serverless application utilizes Amazon Bedrock, an open-source framework for machine learning on AWS, to generate text, translate languages, and write different kinds of creative content. The generated data is then stored in an Amazon S3 bucket for easy access and retrieval.

# Project Structure

* The project contains the following files and folders.

```bash

.
├── README.md                   <-- This instructions file
├── code_genration              <-- Source code for a lambda function that generates code
│   ├── code_genration.py       <-- Lambda function code for generating code programm
├── Image_generation            <-- Source code for a lambda function that generates images
│   ├── image_generation.py     <-- Lambda function code for generating images programm
├── meet_summary                <-- Source code for a lambda function that generates meet summary
│   ├── meeting_summarization.py        <-- Lambda function code for generating meet summary programm

```

# Requirements

* [Python 3 installed](https://www.python.org/downloads/)
* [AWS CLI installed](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
* [AWS IAM permissions configured](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
* [Postman installed](https://www.postman.com/downloads/)

# Setup to create lambda function and layers 

* Command to create lambda functon 

```bash
    aws lambda create-function \
  --function-name my-lambda-function \
  --runtime python3.8 \
  --role arn:aws:iam::123456789012:role/lambda-execution-role \
  --handler index.handler \
  --code fileb://function.zip 
```

* Command to create lambda layer for boto3 library

```bash
    aws lambda publish-layer-version \
  --layer-name my-layer \
  --description "My layer" \
  --content S3Bucket=lambda-layers-us-east-1-123456789012,S3Key=boto3_layer.zip \
    --compatible-runtimes python3.11
```

* Command to create lambda layer for pytz library

```bash
    aws lambda publish-layer-version \
  --layer-name my-layer \
  --description "My layer" \
  --content S3Bucket=lambda-layers-us-east-1-123456789012,S3Key=pytz.zip \
    --compatible-runtimes python3.11
```

# Step to create Api Gateway (HTTP API)

* Command to create Api Gateway (HTTP API)

```bash
    aws apigatewayv2 create-api \
  --name my-api \
  --protocol-type HTTP \
  --target arn:aws:lambda:us-east-1:123456789012:function:my-lambda-function
``` 

# Step to create a s3 bucket in AWS (us-east-1)

* Command to create a s3 bucket in AWS (us-east-1)

```bash
    aws s3api create-bucket \
  --bucket my-bucket \   Name of the bucket unique in AWS 
  --region us-east-1
```
# Step to create a sns topic in AWS (us-east-1)

* Command to create a sns topic in AWS (us-east-1)

```bash
    aws sns create-topic \
  --name my-topic
```

## Do Some Changes in all the py file where 

* Change the bucket name in all the py file where you want to store the data

```bash
    bucket = 'my-bucket' Add your bucket name here 
```
* And change the topic arn in all the py file where you want to store the data

```bash
    topic_arn = 'arn:aws:sns:us-east-1:123456789012:my-topic' Add your topic arn here 
```

## Finally, deploy the application and test it using Postman 

1. Then go to S3 bucket and check the data is stored or not 
2. There will code-output , image-output , meet-summary-output folder in your s3 bucket

# Cleanup

* Delete all the resources created in this project

```bash
    aws lambda delete-function \
  --function-name my-lambda-function
```

```bash
    aws lambda delete-layer-version \
  --layer-name my-layer \
  --version-number 1
```

```bash
    aws apigatewayv2 delete-api \
  --api-id 1234567890
```

```bash
    aws s3api delete-bucket \
  --bucket my-bucket
```

```bash
    aws sns delete-topic \
  --topic-arn arn:aws:sns:us-east-1:123456789012:my-topic
```

# Conclusion

* This project is very useful for the people who are working in the field of machine learning and want to generate code , images and meet summary programmatically. 

Happy Coding smiley 😊😊😊😊 all the best for your future projects.
