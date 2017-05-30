# todo: Check every 5 minutes if there has been a commit in the last 5 minutes? 
# Make a version with infinite loop and test it.
# 5,000 requests per hour on github api when authenticated.
# It takes a few seconds befoore the commit is retrievable from github.

import urllib.request
import re
import json
import os
from datetime import datetime, timedelta, timezone
import smtplib
import time

github_token = ""
github_repo = "test" #Later with environ variable
gmail_user = ""
gmail_pass = ""
gmail_send = ""


def make_request(url):
    request = urllib.request.Request(url)
    request.add_header("Authorization", "token " + github_token)
    response = urllib.request.urlopen(request)
    data = response.read().decode("utf-8")

    return data


def check_times(commit_time, repo, data):
    print("Checking if time: ", (datetime.utcnow().replace(microsecond=0) - timedelta(seconds=10)), "is earlier than: ", commit_time)
    # Create a time for 5 minutes ago and check if the time of the commit is later.
    if (datetime.utcnow().replace(microsecond=0) - timedelta(seconds=10)) <= commit_time:
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
    return

def handler(event, context):

    if os.environ["ENVIRON_A"] != "":
        github_repo = os.environ["ENVIRON_A"]

    print(github_repo)

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
    while 1:
        url = "https://api.github.com/repos/" + repo["owner"]["login"] + "/" +\
               repo["name"] + "/commits"
        # print("Making a request for: ", url)

        data = make_request(url)
        data = json.loads(data)

        commit_time = datetime.strptime(data[0]["commit"]["committer"]["date"], "%Y-%m-%dT%H:%M:%SZ")

        time.sleep(2.0)
        check_times(commit_time, repo, data)

    # Create a time for 5 minutes ago and check if the time of the commit is later.
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