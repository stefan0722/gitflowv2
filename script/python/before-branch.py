#!/usr/bin/python

import subprocess, getpass, os

M2_HOME = os.environ.get("M2_HOME")
PROJECT_HOME = ""
GIT_USER_NAME = ""


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
            if key is "GIT_USER_NAME":
                global GIT_USER_NAME
                GIT_USER_NAME = value


def checkout_branch(branch):
    text = subprocess.check_output(["git","-C",PROJECT_HOME,"checkout",branch]).decode("utf-8")
    print(text + "\n")
    if "git push" in text :
        return True
    return False


def commit_changes():
    eingabe = input("Should the changes be committed to local repository? [Y/N]: ")
    if eingabe is "Y":
        message = input("Please enter commit message: ")
        subprocess.call(["git","-C",PROJECT_HOME,"commit", "-a", "-m", message])


def has_files_to_commit():
    not_committed = subprocess.check_output(["git","-C",PROJECT_HOME,"status","--porcelain","--untracked-files=no"]).decode("utf-8")
    print(not_committed + "\n")
    if not_committed.strip() is not '' :
        return True
    return False


def pull_branch(branch):
    text = subprocess.check_output(["git","-C",PROJECT_HOME,"pull","origin",branch]).decode("utf-8")
    print(text + "\n")
    if "Already up-to-date" in text:
        return True
    return False


def get_remote_url() :
    return subprocess.check_output(["git","-C",PROJECT_HOME,"config","--get","remote.origin.url"]).decode("utf-8").replace("\n","")


def get_username() :
    if "" is GIT_USER_NAME:
        return subprocess.check_output(["git","-C",PROJECT_HOME,"config","--get","user.name"]).decode("utf-8").replace("\n","")
    return GIT_USER_NAME


def push_branch(branch):
    eingabe = input("Should all commits of " + branch + " be pushed to GitHub? [Y/N]: ")
    if eingabe is "Y" :
        remoteUrl = get_remote_url()
        username = get_username()
        password = getpass.getpass("Please enter password for " + remoteUrl + ": ")
        remoteUrl = remoteUrl.replace("https://github.com/","https://" + username + ":" + password + "@github.com/")
        subprocess.check_output(["git","-C",PROJECT_HOME,"push",remoteUrl,branch])
        print("Pulling succesful")
    print("Pulling not done!")


load_environment_var()

print("-- Step 1:     Change local repository to develop branch --")
ahead = checkout_branch("develop")

print("-- Step 2:     Show Status of develop branch --")
has_commits = has_files_to_commit()
if has_commits is True :
    commit_changes()

print("-- Step 3:     Pull current version of develop from GitHub --")
upToDate = pull_branch("develop")

if not upToDate :
    exit("Please check pulled changes and reexecute this script again")

if ahead is True or has_commits is True:
    push_branch("develop")

