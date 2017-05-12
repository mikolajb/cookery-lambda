# File containing all the functions to connect with AWS

import boto3

ACCESS_KEY = ""
SECRET_KEY = ""
REGION = ""
ROLE = ""


# Setup an AWS service.
def setup_client(service):
    client = boto3.client(
        service,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION
    )

    return client


# Check if there already exists a function with the same name,
# otherwise return False.
def check_existing_functions(client, function_name):
    function_list = client.list_functions()
    for i in range(0, len(function_list["Functions"])):
        # todo?: better comparison? http://stackoverflow.com/questions/319426/
        # how-do-i-do-a-case-insensitive-string-comparison-in-python
        if function_list["Functions"][i]["FunctionName"].lower() ==\
           function_name.lower():
                return True

    return False


# Check if the rule already exists, if not return False.
def check_existing_rules(client, rule_name):
    response = client.list_rules(
        NamePrefix=rule_name,
        Limit=100
    )

    if not response["Rules"]:
        return False
    else:
        return True
    return


def set_rule(client, rule_name, number, name):
    response = client.put_rule(
        Name=rule_name,
        ScheduleExpression="rate(" + str(number) + " " + name + ")",
        State="ENABLED",
        Description="Run once every " + str(number) + " " + name,
        RoleArn=ROLE
    )

    print(response)
    return


def upload_to_s3(client, zip_name, bucket_name):
    client.upload_file(zip_name, bucket_name, zip_name)
    print("Uploaded to s3 bucket.")
    return


# Deploy the function to AWS Lambda.
def deploy_lambda(client, dir_to_deploy, function_name, zip_name, file_name,
                  handler_name, bucket_name):

    response = client.create_function(
        FunctionName=function_name,
        Runtime="python3.6",
        Role=ROLE,
        # handler = file_name.handler_function_name
        Handler=dir_to_deploy + "/" + file_name[:-3] + "." + handler_name,
        Code={
            "S3Bucket": bucket_name,
            "S3Key": zip_name
        },
        Description="",
        Timeout=10,
        MemorySize=128,
        Publish=False,
        VpcConfig={
            "SubnetIds": [
            ],
            "SecurityGroupIds": [
            ]
        },
        DeadLetterConfig={
        },
        Environment={
        },
        KMSKeyArn="",
        TracingConfig={
            "Mode": "PassThrough"
        },
        Tags={
        }
    )

    print(response)
    print("Done!")
    return


def apply_rule_to_function(client, rule_name, function_name):
    lambda_client = setup_client("lambda")
    function_arn = lambda_client.get_function(
        FunctionName=function_name)["Configuration"]["FunctionArn"]

    response = client.put_targets(
        Rule=rule_name,
        Targets=[
            {
                'Id': function_name,
                'Arn': function_arn
            },
        ]
    )
    print(response)
    return


def invoke_function(client, function_name):
    response = client.invoke(
        FunctionName=function_name,
        InvocationType="RequestResponse",
        LogType="None"
    )
    result = response["Payload"].read()
    print(result)
    return
