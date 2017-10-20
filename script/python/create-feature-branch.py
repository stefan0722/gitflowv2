#!/usr/bin/python
# Test Comment for rebasing
import os, subprocess, getpass

exec(open("before-branch.py").read())

print("\n\n-- Step 4:     Create new Feature branch locally")
featureBranchName = input("Please enter name of feature branch: feature-")
featureVersion = input("Please enter the version of the feature: ")
alreadyExists = subprocess.call(["git","checkout","-b","feature-" + featureBranchName,"develop"])
if alreadyExists is 128 :
    subprocess.call(["git","checkout","feature-" + featureBranchName],shell=True)

print("\n\n-- Step 5:     Increasing version of feature-" + featureBranchName + " to " + featureVersion + "-SNAPSHOT")
subprocess.call([os.environ.get('M2_HOME')+"/bin/mvn","versions:set",
                 "-f=..//..//",
                 "-DnewVersion="+featureVersion+"-SNAPSHOT","-DprocessAllModules=true",
                 "-DgenerateBackupPoms=false"],shell=True)

print("\n\n-- Step 6:     Commiting update POM Files")
subprocess.call(["git","commit","-m","Change feature branch version to " + featureVersion + "-SNAPSHOT","*pom.xml"])

pushRequest = input("Should the feature branch be pushed to GitHub? [Y/N]: ")
if pushRequest is "Y":
    remoteUrl = subprocess.check_output(["git","config","--get","remote.origin.url"]).decode("utf-8").replace("\n","")
    username = subprocess.check_output(["git","config","--get","user.name"]).decode("utf-8").replace("\n","")
    password = getpass.getpass("Please enter password for " + remoteUrl + ": ")
    remoteUrl = remoteUrl.replace("https://github.com/","https://" + username + ":" + password + "@github.com/")
    subprocess.call(["git","push",remoteUrl,"feature-" + featureBranchName])
