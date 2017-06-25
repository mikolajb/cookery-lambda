# todo: fix dependencies and libraries etc (, with apod-->
# return picture??)

import sys
import os
import aws_connect
import zipfile
# import tempfile
# import gzip

BUCKET_NAME = ""


# Get the paramaters needed for deploying a function.
# Works only if handler file is in top of directory...(check if handler
# function is correct?)
# todo: make it work from everywhere, instead of cwd
# def check_params():
#     if len(sys.argv) < 5:
#         sys.exit("Please run as follows: python3 lambda_deploy.py "
#                  "--directory_to_deploy --function_name --handler_file_name "
#                  "--handler_function_name --optional_environment variables")
#     elif not os.path.isdir("./" + sys.argv[1]):
#         sys.exit("Please specify an existing directory.")
#     elif len(sys.argv[2]) > 64:
#         sys.exit("Please specify a proper function name with max 64 "
#                  "characters.")
#     elif not os.path.isfile("./" + sys.argv[1] + "/" + sys.argv[3]):
#         sys.exit("Please specify an existing handler file name.")
#     elif len(sys.argv) >= 6:
#         # Make for more environmentals.../make a dict from it
#         return (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
#                 sys.argv[5])

#     return (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], "")


# http://stackoverflow.com/questions/1855095/how-to-create-a
# -zip-archive-of-a-directory/
def zip_directory(dir_to_deploy):
    zip_name = dir_to_deploy + "_deploy.zip"
    zip_file = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk("./" + dir_to_deploy):
        for file in files:
            zip_file.write(os.path.join(root, file))
    zip_file.close()
    return zip_name


def remove_zip(zip_name):
    if os.path.isfile(zip_name):
        os.remove(zip_name)
        print("Removed zip file.")
    return


# Does not work...
# def zip_temp(temp, dir_to_deploy):
#     for root, dirs, files in os.walk("./" + dir_to_deploy):
#         for file in files:
#             print(file)
#             with open(os.path.join(root, file), 'r'):
#                 data = os.path.join(root, file).read()
#                 temp.write(gzip.compress(os.path.join(root, file).\
#                   encode('utf-8')))


# if __name__ == "__main__":
def deploy(dir_to_deploy, function_name, file_name, handler_name):
    # (dir_to_deploy, function_name, file_name, handler_name,
    #  environmentals) = check_params()
    environmentals = ""

    lambda_client = aws_connect.setup_client("lambda")
    if aws_connect.check_existing_functions(lambda_client, function_name):
        sys.exit("This function name is already in use.")

    # Block for other zip method, does not work...
    # temp = tempfile.NamedTemporaryFile('wb')
    # temp.name = dir_to_deploy + "_deploy.zip"
    # print(temp.name)
    # zip_temp(temp, dir_to_deploy)

    zip_name = zip_directory(dir_to_deploy)
    s3_client = aws_connect.setup_client("s3")
    aws_connect.upload_to_s3(s3_client, zip_name, BUCKET_NAME)

    # temp.close()

    aws_connect.deploy_lambda(lambda_client, dir_to_deploy, function_name,
                              zip_name, file_name, handler_name, BUCKET_NAME,
                              environmentals)
    remove_zip(zip_name)
    # aws_connect.invoke_function(lambda_client, function_name)
