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
    text = subprocess.check_output(["git","checkout",branch]).decode("utf-8")
    print(text + "\n")
    if "git push" in text :
        return True
    return False


def commit_changes():
    eingabe = input("Should the changes be committed to local repository? [Y/N]: ")
    if eingabe is "Y":
        message = input("Please enter commit message: ")
        subprocess.call(["git", "commit", "-a", "-m", message])


def has_files_to_commit():
    not_committed = subprocess.check_output(["git","status","--porcelain","--untracked-files=no"]).decode("utf-8")
    print(not_committed + "\n")
    if not_committed.strip() is not '' :
        return True
    return False


def pull_branch(branch):
    text = subprocess.check_output(["git","pull","origin",branch]).decode("utf-8")
    print(text + "\n")
    if "Already up-to-date" in text:
        return True
    return False


def push_branch(branch):
    eingabe = input("Should all commits of " + branch + " be pushed to GitHub? [Y/N]: ")
    if eingabe is "Y" :
        remoteUrl = subprocess.check_output(["git","config","--get","remote.origin.url"]).decode("utf-8").replace("\n","")
        username = subprocess.check_output(["git","config","--get","user.name"]).decode("utf-8").replace("\n","")
        password = getpass.getpass("Please enter password for " + remoteUrl + ": ")
        remoteUrl = remoteUrl.replace("https://github.com/","https://" + username + ":" + password + "@github.com/")
        subprocess.call(["git","push",remoteUrl,branch])


print("-- Step 1:     Change local repository to develop branch --")
ahead = checkout_branch("develop")

print("-- Step 2:     Show Status of develop branch --")
has_commits = has_files_to_commit()
if has_commits is True :
    commit_changes()
print("\n\n")

print("-- Step 3:     Pull current version of develop from GitHub --")
upToDate = pull_branch("develop")
print(upToDate)

if not upToDate :
    exit("Please check pulled changes and reexecute this script again")

if ahead is True or has_commits is True:
    push_branch("develop")

