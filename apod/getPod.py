#getPod.py on Lambda server
import urllib
import boto3
import datetime

s3 = boto3.client('s3')

#Gets the picture of the day from the nasa site and stores it in Amazon s3 bucket
def getPod(event, context):

    page = urllib.urlopen(event['url'])

    image_line = ""

    for line in page:
        if ".jpg" in line:
            image_line = line
            break

    ref = image_line.split('"', 2)

    url_pic = "https://apod.nasa.gov/apod/" + ref[1]
    # date = datetime.datetime.now()
    # filename = "nasa%s%s%s.jpg" % (date.day, date.month, date.year)
    filename = event["filename"]
    file_location = "/tmp/" + filename
    
    file = open(file_location, 'w')
    urllib.urlretrieve(url_pic, file_location)
    bucket_name = event["bucketname"]

    s3.upload_file(file_location, bucket_name, filename)
    return 