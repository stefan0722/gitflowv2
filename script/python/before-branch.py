#!/usr/bin/python

import subprocess, getpass

print("-- Step 1:     Change local repository to develop branch --")
ahead = subprocess.check_output(["git","checkout","develop"]).decode("utf-8")
print(ahead + "\n\n")

print("-- Step 2:     Show Status of develop branch --")
notCommited = subprocess.check_output(["git","status","-s"]).decode("utf-8")
print(notCommited + "\n")
if notCommited is not '' :
    eingabe = input("Should the changes be commited to local repository? [Y/N]: ")
    if eingabe is "Y" :
        message = input("Please enter commit message: ")
        subprocess.call(["git","commit","-a","-m",message])
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

