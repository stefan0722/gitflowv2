#!/usr/bin/python

import webbrowser
from helper import gitflow

git_flow_func = gitflow.GitFunctions()

print("\nAvailable local release branches: \n")
git_flow_func.show_branch_state("release")

release_version = input("Please enter name of release branch: release-")
release_branch = "release-" + release_version
git_flow_func.get_clean_branch_state(release_branch)

print("\n-- Step A:     Change local repository to master branch --")
git_flow_func.checkout_branch("master")

print("\n-- Step B:     Pull current version of master from GitHub --")
git_flow_func.pull_branch("master")

print("\n-- Step C:     Change local repository to " + release_branch + " branch --")
git_flow_func.checkout_branch(release_branch)

print("\n-- Step D:     Merge changes from master to " + release_branch +" branch --")
git_flow_func.merge_branch("master")

print("\n-- Step E:     Pushing changes of " + release_branch + " to GitHub --")
git_flow_func.push_branch(release_branch)

print("\n-- Step D:     Open WebBrowser for pull request --")
webbrowser.open_new(git_flow_func.get_remote_url().replace(".git","") + "/compare/master..."
                    + release_branch + "?expand=1")
