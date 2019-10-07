#!/usr/bin/python
# Test Comment for rebasing

from helper import gitflow

git_flow_func = gitflow.GitFunctions()

git_flow_func.get_clean_branch_state("develop")

print("\n\n-- Step 4:     Create new Feature branch locally")
branchName = git_flow_func.checkout_new_branch("feature", "develop")

print("\n-- Current version: " + git_flow_func.get_project_version())
print("\n\n-- Step 5:     Increasing version of " + branchName)
branchVersion = git_flow_func.increase_feature_branch_version()

print("\n\n-- Step 6:     Committing update POM Files to " + branchName)
git_flow_func.commit_changes("Changed " + branchName + " version to " + branchVersion, "**pom.xml")

print("\n\n-- Step 7:     Push changes of " + branchName + " to GutHub")
git_flow_func.push_branch(branchName)
