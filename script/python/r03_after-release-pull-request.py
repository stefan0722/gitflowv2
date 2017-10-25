#!/usr/bin/python

from helper import gitflow

git_flow_func = gitflow.GitFunctions()

print("\nAvailable local release branches: \n")
git_flow_func.show_branch_state("release")

branch_suffix = input("Please enter name of release branch: release-")
branch_name = "release-" + branch_suffix

print("\n-- Step 1:     Change local repository to " + branch_name +" branch --")
git_flow_func.checkout_branch(branch_name)

print("\n-- Step 2:    Run Tests on " + branch_name + " branch --")
git_flow_func.execute_maven_goal("test")

print("\n-- Step 3:       Change local repository to master branch --")
git_flow_func.checkout_branch("master")

print("\n-- Step 4:       Merge " + branch_name + "to master")
git_flow_func.merge_branch_no_ff(branch_name)

print("\n-- Step 5:       Create Tag from master with name v" + branch_suffix)
git_flow_func.create_release_tag(branch_suffix)

print("\n-- Step 6:       Publish master to GitHub")
git_flow_func.push_branch("master")

print("\n-- Step 7:       Publish tag to GitHub")
git_flow_func.push_branch("v" + branch_suffix)

git_flow_func.get_clean_branch_state("develop")

print("\n-- Step 8:       Merge " + branch_name + "to develop")
git_flow_func.merge_branch_no_ff(branch_name)

print("\n-- Current Version: " + git_flow_func.get_project_version())
print("\n-- Step 9:     Increasing version of develop to next version")
git_flow_func.increase_branch_version(True)

print("\n-- Step 10:       Commiting update POM Files to develop branch")
git_flow_func.commit_changes("Changed develop version to SNAPSHOT-VERSION","**pom.xml")

print("\n-- Step 11:       Delete " + branch_name + "branch locally")
git_flow_func.delete_branch_locally(branch_name)

print("\n-- Step 12:       Push the changes with version change to GitHub")
git_flow_func.push_branch("develop")

print("\n-- Step 13:     Change local repository to v"+ branch_suffix +" tag --")
git_flow_func.checkout_branch("v" + branch_suffix)

print("\n-- Step 14:     Call Maven deploy for deploying the tagged result to artifactory --")
# goal = input("Please enter maven goal to be executed [install|deploy]?")
git_flow_func.execute_maven_goal("deploy")

print("\n-- Step 15:     get back to develop --")
git_flow_func.checkout_branch("develop")