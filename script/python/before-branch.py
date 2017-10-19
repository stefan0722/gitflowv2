import subprocess

import os

# exec(open("create-feature-branch.py").read())
# print(os.environ.get('M2_HOME'))
print("-- Step 1:     Change local repository to develop branch --")
ahead = subprocess.check_output(["git","checkout","develop"]).decode("utf-8")
print(ahead)
print()
print()
print("-- Step 2:     Show Status of branch --")
notCommited = subprocess.check_output(["git","status","-s"]).decode("utf-8")
print(notCommited)
print()
print()
if notCommited is not '' :
    eingabe = input("Sollen die Änderungen local commited werden? [Y/N]: ")
    if eingabe is "Y" :
        message = input("Bitte Commit message eingeben: ")
        subprocess.call(["git","commit","-a","-m",message])
print()
print()
print("-- Step 3:     Pull current version of develop from GitHub --")
upToDate = subprocess.check_output(["git","pull","origin","develop"]).decode("utf-8")
print(upToDate)
if "Already up-to-date" not in str(upToDate) :
    exit("Please control and merge develop branch")

if "git push" in ahead or notCommited.splitlines().__sizeof__() > 0 :
    eingabe1 = input("Sollen die Änderungen (Commits) nach develop gepusht werden? [Y/N]")
    if eingabe1 is "Y" :
        subprocess.call(["git","push","origin","develop"])
print()
print()

