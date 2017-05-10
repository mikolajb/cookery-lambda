import urllib
import boto3
import datetime
import tempfile

s3 = boto3.client('s3')


# Gets the picture of the day from the nasa site and stores it in Amazon s3
# bucket
def handler(event, context):

    url = "https://apod.nasa.gov/apod/"
    with urllib.request.urlopen(url) as page:
        text = page.readlines()

    contents = [x.decode('UTF-8') for x in text]

    image_line = ""

    for line in contents:
        if ".jpg" in line:
            image_line = line
            break

    ref = image_line.split('"', 2)

    url_pic = url + "" + ref[1]
    date = datetime.datetime.now()
    file_name = "nasa%s%s%s.jpg" % (date.day, date.month, date.year)
    bucket_name = ""
    # file_name = event["filename"]
    # bucket_name = event["bucketname"]

    # Nested, because flake8 wasn't happy
    # with urllib.request.urlopen(url_pic) as response,
    # tempfile.NamedTemporaryFile('wb') as temp:
    with urllib.request.urlopen(url_pic) as response:
        with tempfile.NamedTemporaryFile('wb') as temp:
            temp.write(response.read())
            s3.upload_file(temp.name, bucket_name, file_name)

    return ("Done! Image can be found in the s3 bucket: " + bucket_name +
            " as: " + file_name)
