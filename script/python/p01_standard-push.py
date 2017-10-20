#!/usr/bin/python

import subprocess, os, getpass

#get current branch name
branchList = subprocess.check_output(["git","branch","--list"]).decode("utf-8")
branchName = ""
for name in branchList.splitlines() :
    if "* " in name :
        branchName = name.replace("* ","")
        break

# Standard Push script
print("-- Step 1:     Commit not commited files --")
notCommited = subprocess.check_output(["git","status","-s"]).decode("utf-8")
if notCommited is not '' :
    eingabe = input("Should the changes be commited to local repository? [Y/N]: ")
    if eingabe is "Y" :
        message = input("Please enter commit message: ")
        subprocess.call(["git","commit","-a","-m",message])

print("-- Step 2:     Pull changes from origin")
errorCode = subprocess.call(["git","pull","origin",branchName])
if errorCode is not 0 :
    exit("Please resolve CONFLICTS and try again")

print("\n-- Step 3:       Increasing version of " + branchName + " branch")
projectDir = input("Please enter project directory: ")
subprocess.call([os.environ.get('M2_HOME')+"/bin/mvn","versions:set",
                 "-f=" + projectDir,
                 "-DnextSnapshot=true",
                 "-DprocessAllModules=true",
                 "-DgenerateBackupPoms=false"],shell=True)

print("\n-- Step 4:       Commiting update POM Files to " + branchName + " branch")
subprocess.call(["git","commit","-m","Change develop branch version to next SNAPSHOT version",projectDir + "**pom.xml"])

print("\n-- Step 5:       Push all changes to GitHub")
eingabe1 = input("Should all commits be pushed to GitHub? [Y/N]: ")
if eingabe1 is "Y" :
    remoteUrl = subprocess.check_output(["git","config","--get","remote.origin.url"]).decode("utf-8").replace("\n","")
    username = subprocess.check_output(["git","config","--get","user.name"]).decode("utf-8").replace("\n","")
    password = getpass.getpass("Please enter password for " + remoteUrl + ": ")
    remoteUrl = remoteUrl.replace("https://github.com/","https://" + username + ":" + password + "@github.com/")
    subprocess.call(["git","push",remoteUrl,branchName])
