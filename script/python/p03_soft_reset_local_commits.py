#!/usr/bin/python

from helper import gitflow

git_flow_func = gitflow.GitFunctions()

commits = int(input("Please enter number of commits: "))
git_flow_func.reset_commits(commits)