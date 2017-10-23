#!/usr/bin/python

import webbrowser

from helper import gitflow

git_flow_func = gitflow.GitFunctions()

print("\nAvailable local feature branches: \n")
git_flow_func.show_branch_state("feature")

featureBranchName = input("Please enter name of feature branch: feature-")
git_flow_func.get_clean_branch_state("feature-" + featureBranchName)

git_flow_func.get_clean_branch_state("develop")

print("\n-- Step A:     Change local repository to feature-"+ featureBranchName +" branch --")
git_flow_func.checkout_branch("feature-" + featureBranchName)

print("\n-- Step B:     Merge develop to feature-"+ featureBranchName +" branch --")
git_flow_func.merge_branch("develop")

print("\n-- Step C:     Pushing changes of feature-" + featureBranchName + " to GitHub --")
git_flow_func.push_branch("feature-" + featureBranchName)

print("\n-- Step D:     Open WebBrowser for pull request --")
webbrowser.open_new(git_flow_func.get_remote_url().replace(".git","") + "/compare/develop...feature-" + featureBranchName+ "?expand=1")
