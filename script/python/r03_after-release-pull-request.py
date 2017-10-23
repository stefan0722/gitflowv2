#!/usr/bin/python
import subprocess, os, getpass

print("\nAvailable local release branches: \n")
subprocess.call(["git","show-branch","--list","release-*"])

releaseVersion = input("Please enter name of release branch: release-")
projectDir = input("Please enter the project directory: ")

print("\n-- Step 1:     Change local repository to release-"+ releaseVersion +" branch --")
ahead = subprocess.check_output(["git","checkout","release-" + releaseVersion],shell=True).decode("utf-8")
print(ahead)
if "git push" in ahead :
    exit("Please push changes to Git hub and finish feature first")

print("\n-- Step 2:    Run Tests on release-" + releaseVersion + " branch --")
subprocess.call([os.environ.get('M2_HOME')+"/bin/mvn","test",
                 "-f=" + projectDir],shell=True)

print("\n-- Step 3:       Change local repository to master branch --")
masterAhead = subprocess.check_output(["git","checkout","master"]).decode("utf-8")
print(masterAhead)
if "git push" in masterAhead :
    exit("Please push changes to Git hub and finish release first")

print("\n-- Step 4:       Merge release-" + releaseVersion + "to master")
subprocess.call(["git","merge","--no-ff","release-" + releaseVersion])

print("\n-- Step 5:       Create Tag from master with name v" + releaseVersion)
subprocess.call(["git","tag","-a","v" + releaseVersion,"-m","Creating Tag for Release v" + releaseVersion])

print("\n-- Step 6:       Publish master to GitHub")
eingabe1 = input("Should all commits be pushed to GitHub? [Y/N]: ")
if eingabe1 is "Y" :
    remoteUrl = subprocess.check_output(["git","config","--get","remote.origin.url"]).decode("utf-8").replace("\n","")
    username = subprocess.check_output(["git","config","--get","user.name"]).decode("utf-8").replace("\n","")
    password = getpass.getpass("Please enter password for " + remoteUrl + ": ")
    remoteUrl = remoteUrl.replace("https://github.com/","https://" + username + ":" + password + "@github.com/")
    subprocess.call(["git","push",remoteUrl,"master"])

print("\n-- Step 7:       Publish tag to GitHub")
eingabe2 = input("Should all commits be pushed to GitHub? [Y/N]: ")
if eingabe2 is "Y" :
    remoteUrl = subprocess.check_output(["git","config","--get","remote.origin.url"]).decode("utf-8").replace("\n","")
    username = subprocess.check_output(["git","config","--get","user.name"]).decode("utf-8").replace("\n","")
    password = getpass.getpass("Please enter password for " + remoteUrl + ": ")
    remoteUrl = remoteUrl.replace("https://github.com/","https://" + username + ":" + password + "@github.com/")
    subprocess.call(["git","push",remoteUrl,"v"+releaseVersion])

exec(open("gitflow.py").read())

print("\n-- Step 8:       Merge release-" + releaseVersion + "to develop")
subprocess.call(["git","merge","--no-ff","release-" + releaseVersion])

print("\n\n-- Step 9:     Increasing version of release-" + releaseVersion + " to " + releaseVersion)
subprocess.call([os.environ.get('M2_HOME')+"/bin/mvn","versions:set",
                 "-f=" + projectDir,
                 "-DnextSnapshot=true",
                 "-DprocessAllModules=true",
                 "-DgenerateBackupPoms=false"],shell=True)

print("\n-- Step 10:       Commiting update POM Files to develop branch")
subprocess.call(["git","commit","-m","Change develop branch version to next SNAPSHOT version",projectDir + "**pom.xml"])

print("\n-- Step 11:       Delete release-" + releaseVersion + "branch locally")
subprocess.call(["git","branch","-d","release-" + releaseVersion])

print("\n-- Step 12:       Push the changes with version change to GitHub")
eingabe1 = input("Should all commits be pushed to GitHub? [Y/N]: ")
if eingabe1 is "Y" :
    remoteUrl = subprocess.check_output(["git","config","--get","remote.origin.url"]).decode("utf-8").replace("\n","")
    username = subprocess.check_output(["git","config","--get","user.name"]).decode("utf-8").replace("\n","")
    password = getpass.getpass("Please enter password for " + remoteUrl + ": ")
    remoteUrl = remoteUrl.replace("https://github.com/","https://" + username + ":" + password + "@github.com/")
    subprocess.call(["git","push",remoteUrl,"develop"])

print("\n-- Step 13:     Change local repository to v"+ releaseVersion +" tag --")
subprocess.call(["git","checkout","v" + releaseVersion],shell=True)

print("\n-- Step 14:     Call Maven deploy for deploying the tagged result to artifactory --")
goal = input("Please enter maven goal to be executed [install|deploy]?")
subprocess.call([os.environ.get('M2_HOME')+"/bin/mvn",goal,
                 "-f=" + projectDir],shell=True)

print("\n-- Step 15:     get back to develop --")
subprocess.call(["git","checkout","develop"],shell=True)