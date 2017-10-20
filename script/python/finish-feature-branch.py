import subprocess

print("\nAvailable local feature branches: \n")
subprocess.call(["git","show-branch","--list","feature-*"])

print("\n-- Step 1:     Change local repository to feature-%feature_branch% branch --")
featureBranchName = input("Please enter name of feature branch: feature-")
subprocess.call(["git","checkout","feature-" + featureBranchName],shell=True)

print("\n-- Step 2:     Commit uncommited changes  --")
notCommited = subprocess.check_output(["git","status","-s"]).decode("utf-8")
if notCommited is not '' :
    eingabe = input("Should the changes be commited to local repository? [Y/N]: ")
    if eingabe is "Y" :
        message = input("Please enter commit message: ")
        subprocess.call(["git","commit","-a","-m",message])

