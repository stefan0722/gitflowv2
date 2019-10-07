#!/usr/bin/python

# Test Comment for rebasing

from helper import gitflow

git_flow_func = gitflow.GitFunctions()

git_flow_func.get_clean_branch_state("develop")

print("\n-- Current version: " + git_flow_func.get_project_version())

print("\n-- Step 5:    Run Tests on develop branch --")
git_flow_func.execute_maven_goal("test")

print("\n-- Step 6:     Create new release branch locally")
release_branch = git_flow_func.checkout_new_branch("release", "develop")

print("\n-- Step 7:     Increasing version of " + release_branch)
release_version = git_flow_func.increase_branch_version(False,str(release_branch).replace("release-",""))

print("\n-- Step 8:     Commiting update POM Files")
git_flow_func.commit_changes("Changed " + release_branch + " version to " + release_version,"**pom.xml")

git_flow_func.push_branch(release_branch)
