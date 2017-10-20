#!/usr/bin/python
import subprocess, getpass, webbrowser

print("\nAvailable local release branches: \n")
subprocess.call(["git","show-branch","--list","release-*"])

releaseVersion = input("Please enter name of release branch: release-")
print("\n-- Step 1:     Change local repository to release-"+ releaseVersion +" branch --")
subprocess.call(["git","checkout","release-" + releaseVersion],shell=True)

notCommited = subprocess.check_output(["git","status","-s"]).decode("utf-8")
if notCommited is not '' :
    eingabe = input("Should the changes be commited to local repository? [Y/N]: ")
    if eingabe is "Y" :
        message = input("Please enter commit message: ")
        subprocess.call(["git","commit","-a","-m",message])

print("\n-- Step 2:     Pull current version of release-" + releaseVersion + " from GitHub --")
upToDate = subprocess.check_output(["git","pull","origin","release-"+ releaseVersion]).decode("utf-8")
if "Already up-to-date" not in str(upToDate) :
    exit("Please check pulled changes and reexecute this script again")

print("\n-- Step 3:     Change local repository to master branch --")
subprocess.call(["git","checkout","master"],shell=True)

print("\n-- Step 4:     Pull current version of master from GitHub --")
upToDate = subprocess.check_output(["git","pull","origin","master"]).decode("utf-8")
if "Already up-to-date" not in str(upToDate) :
    exit("Please check pulled changes and reexecute this script again")

print("\n-- Step 5:     Change local repository to release-"+ releaseVersion +" branch --")
subprocess.call(["git","checkout","release-" + releaseVersion],shell=True)

print("\n-- Step 6:     Merge changes from master to release-"+ releaseVersion +" branch --")
mergeResult = subprocess.call(["git","merge","master"])
if mergeResult is 1 :
    exit("Please resolve conflict before continue")

print("-- Step 7:     Pushing changes of release-" + releaseVersion + " to GitHub --")
eingabe1 = input("Should all commits be pushed to GitHub? [Y/N]: ")
if eingabe1 is "Y" :
    remoteUrl = subprocess.check_output(["git","config","--get","remote.origin.url"]).decode("utf-8").replace("\n","")
    username = subprocess.check_output(["git","config","--get","user.name"]).decode("utf-8").replace("\n","")
    password = getpass.getpass("Please enter password for " + remoteUrl + ": ")
    remoteUrl = remoteUrl.replace("https://github.com/","https://" + username + ":" + password + "@github.com/")
    subprocess.call(["git","push",remoteUrl,"release-" + releaseVersion])

    print("Please Open Pull Request")
    webbrowser.open_new(remoteUrl + "/compare/master...release-" + releaseVersion+ "?expand=1")
