#!/usr/bin/python
# Test Comment for rebasing

from helper import gitflow

gitflowfunc = gitflow.GitFunctions()

gitflowfunc.get_clean_branch_state("develop")

print("\n\n-- Step 4:     Create new Feature branch locally")
branchName = gitflowfunc.checkout_new_branch("feature","develop")

print("\n\n-- Step 5:     Increasing version of " + branchName)
branchVersion = gitflowfunc.increase_branch_version()

print("\n\n-- Step 6:     Committing update POM Files to " + branchName)
gitflowfunc.commit_changes("Changed " + branchName + " version to " + branchVersion,"**pom.xml")

print("\n\n-- Step 7:     Push changes of " + branchName + " to GutHub")
gitflowfunc.push_branch(branchName)
