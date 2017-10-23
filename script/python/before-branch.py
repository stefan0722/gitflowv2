#!/usr/bin/python

import subprocess, getpass, os

M2_HOME = os.environ.get("M2_HOME")
PROJECT_HOME = ""


def load_environment_var() :
    with open("environment.txt","r") as f:
        for line in f.read().splitlines() :
            elements = line.split('=')
            key = elements[0]
            value = elements[1]
            if key is "M2_HOME":
                global M2_HOME
                M2_HOME = value
            if key is "PROJECT_HOME":
                global PROJECT_HOME
                PROJECT_HOME = value


def checkout_branch(branch):
    return subprocess.check_output(["git","checkout",branch]).decode("utf-8")


def commit_changes():
    not_commited = subprocess.check_output(["git","status","-s"]).decode("utf-8")
    print(not_commited + "\n")
    if not_commited is not '' :
        eingabe = input("Should the changes be commited to local repository? [Y/N]: ")
        if eingabe is "Y" :
            message = input("Please enter commit message: ")
            subprocess.call(["git","commit","-a","-m",message])


print("-- Step 1:     Change local repository to develop branch --")
ahead = checkout_branch("develop")
print(ahead + "\n\n")

print("-- Step 2:     Show Status of develop branch --")
commit_changes()
print("\n\n")

print("-- Step 3:     Pull current version of develop from GitHub --")
upToDate = subprocess.check_output(["git","pull","origin","develop"]).decode("utf-8")
print(upToDate)

if "Already up-to-date" not in str(upToDate) :
    exit("Please check pulled changes and reexecute this script again")

if "git push" in ahead or notCommited is not '':
    eingabe1 = input("Should all commits of develop be pushed to GitHub? [Y/N]: ")
    if eingabe1 is "Y" :
        remoteUrl = subprocess.check_output(["git","config","--get","remote.origin.url"]).decode("utf-8").replace("\n","")
        username = subprocess.check_output(["git","config","--get","user.name"]).decode("utf-8").replace("\n","")
        password = getpass.getpass("Please enter password for " + remoteUrl + ": ")
        remoteUrl = remoteUrl.replace("https://github.com/","https://" + username + ":" + password + "@github.com/")
        subprocess.call(["git","push",remoteUrl,"develop"])

