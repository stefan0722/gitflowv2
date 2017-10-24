#!/usr/bin/python

from helper import gitflow

git_flow_func = gitflow.GitFunctions()

#get current branch name
current_branch = git_flow_func.get_current_branch_name()

# Standard Push script
print("-- Step 1:     Commit not commited files --")
has_commits = git_flow_func.has_files_to_commit()
if has_commits is True:
    git_flow_func.commit_changes()

print("-- Step 2:     Pull changes from origin")
git_flow_func.pull_branch(current_branch)

print("\n-- Step 3:       Increasing version of " + current_branch + " branch")
git_flow_func.increase_branch_version_next_snapshot()

print("\n-- Step 4:       Commiting update POM Files to " + current_branch + " branch")
git_flow_func.commit_changes("Change " + current_branch + " version to next SNAPSHOT version","**pom.xml")

print("\n-- Step 5:       Push all changes to GitHub")
git_flow_func.push_branch(current_branch)
