import urllib
import boto3
import datetime

s3 = boto3.client('s3')

#Gets the picture of the day from the nasa site and stores it in Amazon s3 bucket
def handler(event, context):

	url = "https://apod.nasa.gov/apod/"
	page = urllib.urlopen(url)

	image_line = ""

	for line in page:
		if ".jpg" in line:
			image_line = line
			break

	ref = image_line.split('"', 2)

	url_pic = url + "" + ref[1]
	date = datetime.datetime.now()
	file_name = "nasa%s%s%s.jpg" % (date.day, date.month, date.year)
	# file_name = event["filename"]
	file_location = "/tmp/" + file_name
	
	f = open(file_location, 'w')
	urllib.urlretrieve(url_pic, file_location)
	f.close()
	# bucket_name = event["bucketname"]
	bucket_name = "apodresult"

	s3.upload_file(file_location, bucket_name, file_name)
	return ("Done! Image can be found in the s3 bucket: " + bucket_name + " as: " + file_name)