# todo: fix dependencies and libraries etc, check handler (name, form etc..) and get names of handler and file

import sys
import os
import boto3
import zipfile

ACCESS_KEY = "***REMOVED***"
SECRET_KEY = "***REMOVED***"
REGION = "eu-central-1"
BUCKET_NAME = "***REMOVED***"

# todo: make it work from everywhere, instead of cwd
def getDirToDeploy():
	if (len(sys.argv) < 2 or not os.path.isdir("./" + sys.argv[1])):
		sys.exit("Please specify an existing directory.")
	else:
		return sys.argv[1]

def getFunctionName():
	if (len(sys.argv) < 3 or len(sys.argv[2]) > 64):
		sys.exit("Please specify a proper function name with max 64 characters.")
	else:
		return sys.argv[2]

def setupLambdaClient():
	client = boto3.client("lambda",
		aws_access_key_id = ACCESS_KEY,
		aws_secret_access_key = SECRET_KEY,
		region_name = REGION)

	return client

def setupS3Client():
	client = boto3.client("s3",
		aws_access_key_id = ACCESS_KEY,
		aws_secret_access_key = SECRET_KEY,
		region_name = REGION)

	return client

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

def deployLambda(client, dir_to_deploy, function_name, zip_name):
	response = client.create_function(
		FunctionName = function_name,
		Runtime = "python3.6",
		Role = "arn:aws:iam::151587718953:role/service-role/testRole",
		Handler = zip_name[:4] + "/test.testHandler",
		Code = {
			"S3Bucket": BUCKET_NAME,
			"S3Key": zip_name
		},
		Description = "",
		Timeout = 3,
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
	print(response)
	print("Done!")

if __name__ == "__main__":
	dir_to_deploy = getDirToDeploy()
	function_name = getFunctionName()

	lambda_client = setupLambdaClient()
	checkExistingFunctions(lambda_client, function_name)

	zip_name = zipDirectory(dir_to_deploy)
	s3_client = setupS3Client()
	uploadToS3(s3_client, zip_name, BUCKET_NAME)
	deployLambda(lambda_client, dir_to_deploy, function_name, zip_name)
