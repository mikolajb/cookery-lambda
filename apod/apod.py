import urllib
import cStringIO
import Image

def get_picture(url):
    # urllib.urlretrieve(url, "nasa1.jpg")
    page = urllib.urlopen(url)

    image_line = ""

    for line in page:
        if ".jpg" in line:
            # print line
            image_line = line
            break


    print image_line
    ref = image_line.split('"', 2)
    print ref[1]


    # wiki apod parser
    # print image_line
    # ref = image_line.split('"', 10)
    # print ref[9]
    # res_line = ref[9]
    # res_line = res_line.split(".jpg")
    # url_pic = "https://" + res_line[0][2:] + ".jpg"
    # url_pic = url_pic.replace("thumb/", "")
    # print url_pic

    # if ref[1].startswith("/wiki"):
    #   ref[1] = ref[1][5:]
    #   print "BANAAN"

    # print ref[1]

    # url_pic = "https://apod.nasa.gov/apod/" + ref[1]
    # url_pic = "https://upload.wikimedia.org/wikipedia/commons/6/6b/Sidney_Hall_-_Urania%27s_Mirror_-_Cassiopeia_%28image_right_side_up%29.jpg"
    # print url_pic

    # img_file = cStringIO.StringIO(urllib.urlopen(url_pic).read())
    # Image.open(img_file).show()

    urllib.urlretrieve(url_pic, "1.jpg")

if __name__ == "__main__":
    url_nasa = "https://apod.nasa.gov/apod/astropix.html"
    url_wiki = "https://en.wikipedia.org/wiki/Wikipedia:Picture_of_the_day"
    get_picture(url_wiki)


    def getPod(event, context):
    page = urllib.urlopen(event['url'])

    image_line = ""

    for line in page:
        if ".jpg" in line:
            # print line
            image_line = line
            break

    print image_line
    ref = image_line.split('"', 2)
    print ref[1]

    url_pic = "https://apod.nasa.gov/apod/" + ref[1]
    img_file = cStringIO.StringIO(urllib.urlopen(url_pic).read())
    Image.open(img_file).show()


    # Jupyter notebook...
    #     %matplotlib inline

    # import matplotlib.pyplot as plt
    # import matplotlib.image as mpimg
    # from PIL import Image
    # import boto3
    # import datetime

    # access_key = "***REMOVED***"
    # secret_key = "***REMOVED***"

    # date = datetime.datetime.now()
    # filename = "nasa%s%s%s.jpg" % (date.day, date.month, date.year)
    # bucketname = "apodresult"
    # url = "https://apod.nasa.gov/apod/"

    # client = boto3.client("s3",
    #     aws_access_key_id = access_key,
    #     aws_secret_access_key = secret_key,
    #     region_name = "eu-central-1",
    # )
    # resource = boto3.resource(
    #     "s3",
    #     aws_access_key_id = access_key,
    #     aws_secret_access_key = secret_key,
    #     region_name = "eu-central-1",
    # )



    # resource.meta.client.download_file("apodresult", filename, filename)
    # Show image inline...
    # img = mpimg.imread(filename)
    # imgplot = plt.imshow(img)
    # plt.show()

    # show image extern...
    # img = Image.open(filename)
    # img.show()