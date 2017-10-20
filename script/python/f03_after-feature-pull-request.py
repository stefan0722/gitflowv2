import subprocess, os, getpass

print("\nAvailable local feature branches: \n")
subprocess.call(["git","show-branch","--list","feature-*"])

featureBranchName = input("Please enter name of feature branch: feature-")
projectDir = input("Please enter the project directory: ")

print("\n-- Step 1:     Change local repository to feature-"+ featureBranchName +" branch --")
ahead = subprocess.check_output(["git","checkout","feature-" + featureBranchName],shell=True).decode("utf-8")
print(ahead)
if "git push" in ahead :
    exit("Please push changes to Git hub and finish feature first")

print("\n-- Step 2:    Run Tests on feature-" + featureBranchName + " branch --")
subprocess.call([os.environ.get('M2_HOME')+"/bin/mvn","test",
                 "-f=" + projectDir],shell=True)

print("\n-- Step 3:       Change local repository to develop branch --")
devAhead = subprocess.check_output(["git","checkout","develop"]).decode("utf-8")
print(devAhead)
if "git push" in devAhead :
    exit("Please push changes to Git hub and finish feature first")

print("\n-- Step 4:       Merge feature-" + featureBranchName + "to develop")
subprocess.call(["git","merge","--no-ff","feature-" + featureBranchName])

print("\n-- Step 5:       Delete feature-" + featureBranchName + "branch locally")
subprocess.call(["git","branch","-d","feature-" + featureBranchName])

print("\n-- Step 6:       Increasing version of develop branch")
subprocess.call([os.environ.get('M2_HOME')+"/bin/mvn","versions:set",
                 "-f=" + projectDir,
                 "-DnextSnapshot=true",
                 "-DprocessAllModules=true",
                 "-DgenerateBackupPoms=false"],shell=True)

print("\n-- Step 7:       Commiting update POM Files to develop branch")
subprocess.call(["git","commit","-m","Change develop branch version to next SNAPSHOT version",projectDir + "**pom.xml"])

print("\n-- Step 8:       Push the changes with version change to GitHub")
eingabe1 = input("Should all commits be pushed to GitHub? [Y/N]: ")
if eingabe1 is "Y" :
    remoteUrl = subprocess.check_output(["git","config","--get","remote.origin.url"]).decode("utf-8").replace("\n","")
    username = subprocess.check_output(["git","config","--get","user.name"]).decode("utf-8").replace("\n","")
    password = getpass.getpass("Please enter password for " + remoteUrl + ": ")
    remoteUrl = remoteUrl.replace("https://github.com/","https://" + username + ":" + password + "@github.com/")
    subprocess.call(["git","push",remoteUrl,"develop"])
