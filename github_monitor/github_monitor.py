# todo: Functions retries after failure, so need to terminate
# Make a version with infinite loop and test it.
# 5,000 requests per hour on github api when authenticated.
# It takes a few seconds befoore the commit is retrievable from github and
# for sending the mail.
# Takes a while to reboot lambda function, so need bigger interval.
# This function consider commits that are pushed immediately.
# Functions that are run on laptop act normal, but on lambda functions can be
# "stuck"

import urllib.request
import json
from datetime import datetime, timedelta
import smtplib
import time

github_token = ""
github_repo = "test"  # Later with environ variable
gmail_user = ""
gmail_pass = ""
gmail_send = ""


# Makes an authorized request to github.
def make_request(url):
    request = urllib.request.Request(url)
    request.add_header("Authorization", "token " + github_token)
    response = urllib.request.urlopen(request)
    data = response.read().decode("utf-8")

    return data


def check_times(commit_time, now, repo, data):
    print("Checking if time: ", (now - timedelta(seconds=70)),
          "is earlier than: ", commit_time)
    # Create a time for 5 minutes ago and check if the time
    # of the commit is later.
    if (now - timedelta(seconds=70)) <= commit_time:
        # Found new commit, so mail details..
        url = "https://api.github.com/repos/" + repo["owner"]["login"] + "/" +\
           repo["name"] + "/commits/" + data[0]["sha"]
        # print("Making a request for: ", url)

        data = make_request(url)
        data = json.loads(data)

        send_email(data)
        print("Mail sent!")

    return


def send_email(data):
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login(gmail_user, gmail_pass)

    content = "The Github Monitor found a new commit in the repository: " +\
              github_repo + ".\nIn total there are " +\
              str(data["stats"]["total"]) + " changes: " +\
              str(data["stats"]["additions"]) + " additions and " +\
              str(data["stats"]["deletions"]) + " deletions.\n\n"

    for i, item in enumerate(data["files"]):
        content += "The changes in " + item["filename"] + ":\n" +\
                    item["patch"] + "\n\n"

    content += "The full commit can be found at: " + data["html_url"]

    # Send the mail
    msg = "\r\n".join([
        "From: " + gmail_user,
        "To: " + gmail_send,
        "Subject: [Github Monitor]",
        "",
        content
        ])
    server.sendmail(gmail_user, gmail_send, msg)
    server.quit()
    return


def handler(event, context):

    # if os.environ["ENVIRON_A"] != "":
    #     github_repo = os.environ["ENVIRON_A"]

    url = "https://api.github.com/user/repos"
    data = make_request(url)

    repos = json.loads(data)

    # check for existing repos. if not mail a warning
    repo = {}
    for i, item in enumerate(repos):
        if item["name"] == github_repo:
            repo = item
            break

    if repo == {}:
        print("WARNING: NON EXISTENT REPOSITORY")
        return

    # get all commits
    count = 0
    while count < 5:
        now = datetime.utcnow().replace(microsecond=0)
        url = "https://api.github.com/repos/" + repo["owner"]["login"] + "/" +\
              repo["name"] + "/commits"
        # print("Making a request for: ", url)

        data = make_request(url)
        data = json.loads(data)

        commit_time = datetime.strptime(data[0]["commit"]["committer"]["date"],
                                        "%Y-%m-%dT%H:%M:%SZ")

        check_times(commit_time, now, repo, data)
        time.sleep(59.0)
        count += 1

    # Create a time for 5 minutes ago and check if the time of the commit is
    # later.
    # if (datetime.utcnow() - timedelta(minutes=5)) < commit_time:
    #     # Found new commit, so mail details..
    #     url = "https://api.github.com/repos/" + repo["owner"]["login"] + "/" +\
    #        repo["name"] + "/commits/" + data[0]["sha"]
    #     # print("Making a request for: ", url)

    #     data = make_request(url)
    #     data = json.loads(data)

    #     send_email(data)

    return


if __name__ == "__main__":
    handler(0, 0)
