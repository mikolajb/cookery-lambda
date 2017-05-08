# todo: fix dependencies and libraries etc, set schedule(, with apod--> return picture??)

import sys
import os
import boto3
import zipfile

ACCESS_KEY = ""
SECRET_KEY = ""
REGION = "eu-central-1"
BUCKET_NAME = ""

# Get the paramaters needed for deploying a function.
# Works only if handler file is in top of directory...(check if handler function is correct?)
# todo: make it work from everywhere, instead of cwd
def getParams():
	if len(sys.argv) < 5:
		sys.exit("Please run as follows: python3 --directory_to_deploy --function_name --handler_file_name --handler_function_name")
	elif not os.path.isdir("./" + sys.argv[1]):
		sys.exit("Please specify an existing directory.")
	elif len(sys.argv[2]) > 64:
		sys.exit("Please specify a proper function name with max 64 characters.")
	elif not os.path.isfile("./" + sys.argv[1] + "/" + sys.argv[3]):
		sys.exit("Please specify an existing handler file name.")

	return (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

# Setup an AWS service.
def setupClient(service):
	client = boto3.client(service,
		aws_access_key_id = ACCESS_KEY,
		aws_secret_access_key = SECRET_KEY,
		region_name = REGION)

	return client

# Check if there already exists a function with the same name.
def checkExistingFunctions(client, function_name):
	function_list = client.list_functions()
	for i in range(0, len(function_list["Functions"])):
		# todo?: better comparison? http://stackoverflow.com/questions/319426/how-do-i-do-a-case-insensitive-string-comparison-in-python
		if function_list["Functions"][i]["FunctionName"].lower() == function_name.lower():
			sys.exit("This function name is already in use.")

	return

# http://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory/
def zipDirectory(dir_to_deploy):
	zip_name = dir_to_deploy + "_deploy.zip"
	zip_file = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
	for root, dirs, files in os.walk("./" + dir_to_deploy):
		for file in files:
			zip_file.write(os.path.join(root, file))
	zip_file.close()
	return zip_name

def uploadToS3(client, zip_name, bucket_name):
	client.upload_file(zip_name, bucket_name, zip_name)
	return

def invokeFunction(client, function_name):
	response = client.invoke(
		FunctionName = function_name,
		InvocationType = "RequestResponse",
		LogType = "None"
	)
	result = response["Payload"].read()
	print(result)
	return

# Deploy the function to AWS Lambda.
def deployLambda(client, dir_to_deploy, function_name, zip_name, file_name, handler_name):
	response = client.create_function(
		FunctionName = function_name,
		Runtime = "python2.7",
		Role = "arn:aws:iam::151587718953:role/service-role/testRole",
		Handler = dir_to_deploy + "/" + file_name[:-3] + "." + handler_name, # handler = file_name.handler_function_name
		Code = {
			"S3Bucket": BUCKET_NAME,
			"S3Key": zip_name
		},
		Description = "",
		Timeout = 10,
		MemorySize = 128,
		Publish = False,
		VpcConfig = {
			"SubnetIds": [
			],
			"SecurityGroupIds": [
			]
		},
		DeadLetterConfig = {
		},
		Environment = {
		},
		KMSKeyArn = "",
		TracingConfig = {
			"Mode": "PassThrough"
		},
		Tags = {
		}
	)
	# print(response)
	print("Done!")

if __name__ == "__main__":
	(dir_to_deploy, function_name, file_name, handler_name) = getParams()

	lambda_client = setupClient("lambda")
	checkExistingFunctions(lambda_client, function_name)

	zip_name = zipDirectory(dir_to_deploy)
	s3_client = setupClient("s3")
	uploadToS3(s3_client, zip_name, BUCKET_NAME)
	deployLambda(lambda_client, dir_to_deploy, function_name, zip_name, file_name, handler_name)
	invokeFunction(lambda_client, function_name)