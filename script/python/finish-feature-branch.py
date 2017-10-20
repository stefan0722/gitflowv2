import subprocess

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

print("-- Step 2:     Pull current version of feature-%feature_branch% from GitHub --")
upToDate = subprocess.check_output(["git","pull","origin","feature-"+ featureBranchName]).decode("utf-8")
