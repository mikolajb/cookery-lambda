# todo: fix dependencies and libraries etc, upload zip, check handler (name, form etc..)
# todo: Cant fix encoding of zip file or sending zip file, so trying uploading to s3 instead.

import sys
import os
import boto3
import zipfile
import base64

ACCESS_KEY = "***REMOVED***"
SECRET_KEY = "***REMOVED***"
REGION = "eu-central-1"

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
# todo: fix this so aws lambda recognizes it, because zipping more than 1 file results in a directory----
# FIXED: Doesnt matter...
def zipDirectory(dir_to_deploy):
	zip_file = zipfile.ZipFile((dir_to_deploy + "ing.zip"), 'w', zipfile.ZIP_DEFLATED)
	for root, dirs, files in os.walk("./" + dir_to_deploy):
		for file in files:
			zip_file.write(os.path.join(root, file))
	zip_file.close()
	return

# "the contents of the zip file must be base64-encoded"
# def encode():
# 	print(os.getcwd())
# 	fin = open("test/test.py")
# 	fout = open("test/test.b64")
# 	with open('test.zip', 'rb') as fin, open('test.zip.b64', 'w') as fout:
# 		base64.encode(fin, fout)
# 	base64.encode(f, open("test/test.b64", "w"))
# 	f.close()

def uploadToS3(client):
	client.upload_file("testing.zip", "***REMOVED***", "testing.zip")

def deployLambda(client, dir_to_deploy, function_name):
	name = (dir_to_deploy + "ing.zip")
	response = client.create_function(
		FunctionName = function_name,
		Runtime = "python3.6",
		Role = "arn:aws:iam::151587718953:role/service-role/testRole",
		Handler = "test.testHandler",
		Code = {
			# "ZipFile": file_get_contents(str(dir_to_deploy + ".zip"))
			"S3Bucket": "***REMOVED***",
			"S3Key": "testing.zip"
			# 'S3ObjectVersion': 'string'
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

def file_get_contents(filename):
	with open(filename) as f:
		return f.read()

if __name__ == "__main__":
	dir_to_deploy = getDirToDeploy()
	function_name = getFunctionName()

	lambda_client = setupLambdaClient()
	checkExistingFunctions(lambda_client, function_name)

	# encode()
	zipDirectory(dir_to_deploy)
	s3_client = setupS3Client()
	uploadToS3(s3_client)
	deployLambda(lambda_client, dir_to_deploy, function_name)