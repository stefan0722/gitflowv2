#!/usr/bin/python
# Test Comment for rebasing
import os, subprocess, getpass

exec(open("before-branch.py").read())

projectDir = input("Please enter the project directory: ")

print("\n\n-- Step 4:     Create new Release branch locally")
releaseVersion = input("Please enter the version of the release: ")
alreadyExists = subprocess.call(["git","checkout","-b","release-" + releaseVersion,"develop"])
if alreadyExists is 128 :
    subprocess.call(["git","checkout","feature-" + releaseVersion],shell=True)

print("\n\n-- Step 5:     Increasing version of release-" + releaseVersion + " to " + releaseVersion)
subprocess.call([os.environ.get('M2_HOME')+"/bin/mvn","versions:set",
                 "-f=" + projectDir,
                 "-DnewVersion="+releaseVersion,"-DprocessAllModules=true",
                 "-DgenerateBackupPoms=false"],shell=True)

print("\n\n-- Step 6:     Commiting update POM Files")
subprocess.call(["git","commit","-m","Change release branch version to " + releaseVersion,projectDir + "**pom.xml"])

pushRequest = input("Should the release branch be pushed to GitHub? [Y/N]: ")
if pushRequest is "Y":
    remoteUrl = subprocess.check_output(["git","config","--get","remote.origin.url"]).decode("utf-8").replace("\n","")
    username = subprocess.check_output(["git","config","--get","user.name"]).decode("utf-8").replace("\n","")
    password = getpass.getpass("Please enter password for " + remoteUrl + ": ")
    remoteUrl = remoteUrl.replace("https://github.com/","https://" + username + ":" + password + "@github.com/")
    subprocess.call(["git","push",remoteUrl,"release-" + releaseVersion])
