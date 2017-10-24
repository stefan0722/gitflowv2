#!/usr/bin/python

from helper import gitflow

git_flow_func = gitflow.GitFunctions()

print("\nAvailable local feature branches: \n")
git_flow_func.show_branch_state("feature")

branch_suffix = input("Please enter name of feature branch: feature-")
featureBranchName = "feature-" + branch_suffix
git_flow_func.get_clean_branch_state(featureBranchName)

print("\n-- Step 2:    Run Tests on " + featureBranchName + " branch --")
git_flow_func.execute_maven_goal("test")

print("\n-- Step 3:       Change local repository to develop branch --")
git_flow_func.get_clean_branch_state("develop")

print("\n-- Step 4:       Merge " + featureBranchName + "to develop")
git_flow_func.merge_branch_no_ff(featureBranchName)

print("\n-- Step 5:       Delete " + featureBranchName + "branch locally")
git_flow_func.delete_branch_locally(featureBranchName)

print("\n-- Step 6:       Increasing version of develop branch")
git_flow_func.increase_branch_version_next_snapshot()

print("\n-- Step 7:       Committing update POM Files to develop branch")
git_flow_func.commit_changes("Change develop branch version to next SNAPSHOT version","**pom.xml")

print("\n-- Step 8:       Push the changes with version change to GitHub")
git_flow_func.push_branch("develop")
