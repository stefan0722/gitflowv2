import subprocess, getpass, webbrowser

print("\nAvailable local feature branches: \n")
subprocess.call(["git","show-branch","--list","feature-*"])

featureBranchName = input("Please enter name of feature branch: feature-")
print("\n-- Step 1:     Change local repository to feature-"+ featureBranchName +" branch --")
subprocess.call(["git","checkout","feature-" + featureBranchName],shell=True)

notCommited = subprocess.check_output(["git","status","-s"]).decode("utf-8")
if notCommited is not '' :
    eingabe = input("Should the changes be commited to local repository? [Y/N]: ")
    if eingabe is "Y" :
        message = input("Please enter commit message: ")
        subprocess.call(["git","commit","-a","-m",message])

print("-- Step 2:     Pull current version of feature-" + featureBranchName + " from GitHub --")
upToDate = subprocess.check_output(["git","pull","origin","feature-"+ featureBranchName]).decode("utf-8")
if "Already up-to-date" not in str(upToDate) :
    exit("Please check pulled changes and reexecute this script again")

# Bring develop branch in sync
exec(open("before-branch.py").read())

print("\n-- Step 3:     Change local repository to feature-"+ featureBranchName +" branch --")
subprocess.call(["git","checkout","feature-" + featureBranchName],shell=True)

print("\n-- Step 4:     Change local repository to feature-"+ featureBranchName +" branch --")
mergeResult = subprocess.check_output(["git","merge","develop"]).decode("utf-8")
print(mergeResult+ "\n")
if "CONFLICT" in mergeResult :
    exit("Please resolve conflict before continue")

print("-- Step 5:     Pushing changes of feature-" + featureBranchName + " to GitHub --")
eingabe1 = input("Should all commits be pushed to GitHub? [Y/N]: ")
if eingabe1 is "Y" :
    remoteUrl = subprocess.check_output(["git","config","--get","remote.origin.url"]).decode("utf-8").replace("\n","")
    username = subprocess.check_output(["git","config","--get","user.name"]).decode("utf-8").replace("\n","")
    password = getpass.getpass("Please enter password for " + remoteUrl + ": ")
    remoteUrl = remoteUrl.replace("https://github.com/","https://" + username + ":" + password + "@github.com/")
    subprocess.call(["git","push",remoteUrl,"feature-" + featureBranchName])

    print("Please Open Pull Request")
    webbrowser.open_new(remoteUrl + "/compare/feature-" + featureBranchName+ "?expand=1")
