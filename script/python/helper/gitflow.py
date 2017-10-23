#!/usr/bin/python

import subprocess
import getpass
import os


class GitFunctions:
    PROJECT_HOME = None
    GIT_USER_NAME = None
    M2_HOME = os.environ.get("M2_HOME")
    GIT_PASSWORD = None

    def __init__(self):
        self.load_environment_var()
        self.get_project_home()

    def load_environment_var(self):
        with open("environment.txt", "r") as f:
            for line in f.read().splitlines():
                elements = line.split('=')
                key = elements[0]
                value = elements[1]
                if key is "M2_HOME":
                    self.M2_HOME = value
                if "PROJECT_HOME" in key:
                    self.PROJECT_HOME = value
                if "GIT_USER_NAME" in key:
                    self.GIT_USER_NAME = value

    def checkout_branch(self, branch):
        text = subprocess.check_output(["git", "-C", self.PROJECT_HOME, "checkout", branch]).decode("utf-8")
        print(text + "\n")
        if "git push" in text:
            return True
        return False

    def checkout_new_branch(self, branch_prefix, from_branch):
        branch_name = input("Please enter name of branch: " + branch_prefix + "-")
        complete_branch_name = branch_prefix + "-" + branch_name
        already_exists = subprocess.call(
            ["git", "-C", self.PROJECT_HOME, "checkout", "-b", complete_branch_name, from_branch])
        if already_exists is 128:
            subprocess.call(["git", "-C", self.PROJECT_HOME, "checkout", complete_branch_name], shell=True)
        return complete_branch_name

    def increase_branch_version(self, is_snapshot=True):
        version = input("Please enter the new version: ")
        if is_snapshot:
            version = version + "-SNAPSHOT"
        subprocess.call([self.M2_HOME + "/bin/mvn", "versions:set",
                         "-f=" + self.PROJECT_HOME,
                         "-DnewVersion=" + version, "-DprocessAllModules=true",
                         "-DgenerateBackupPoms=false"], shell=True)
        return version

    def commit_changes(self, message=None, file_pattern=None):
        entry = input("Should the changes be committed to local repository? [Y/N]: ")
        if entry is "Y":
            if message is None:
                message = input("Please enter commit message: ")
            if file_pattern is None:
                subprocess.call(["git", "-C", self.PROJECT_HOME, "commit", "-a", "-m", message])
                return
            subprocess.call(["git", "-C", self.PROJECT_HOME, "commit", "-m", message, self.PROJECT_HOME +
                             file_pattern])

    def has_files_to_commit(self):
        not_committed = subprocess.check_output(
            ["git", "-C", self.PROJECT_HOME, "status", "--porcelain", "--untracked-files=no"]).decode("utf-8")
        print(not_committed + "\n")
        if not_committed.strip() is not '':
            return True
        return False

    def pull_branch(self, branch):
        text = subprocess.check_output(["git", "-C", self.PROJECT_HOME, "pull", "origin", branch]).decode("utf-8")
        print(text + "\n")
        if "Already up-to-date" in text:
            return True
        return False

    def get_remote_url(self):
        return subprocess.check_output(["git", "-C", self.PROJECT_HOME, "config", "--get", "remote.origin.url"]).decode(
            "utf-8").replace("\n", "")

    def get_username(self):
        if self.GIT_USER_NAME is None:
            return subprocess.check_output(["git", "-C", self.PROJECT_HOME, "config", "--get", "user.name"]).decode(
                "utf-8").replace("\n", "")
        return self.GIT_USER_NAME

    def push_branch(self, branch):
        entry = input("Should all commits of " + branch + " be pushed to GitHub? [Y/N]: ")
        if entry is "Y":
            remote_url = GitFunctions.get_remote_url(self)
            username = GitFunctions.get_username(self)
            if self.GIT_PASSWORD is None:
                self.GIT_PASSWORD = getpass.getpass("Please enter password for " + remote_url + ": ")
            remote_url = remote_url.replace("https://github.com/",
                                            "https://" + username + ":" + self.GIT_PASSWORD + "@github.com/")
            subprocess.check_output(["git", "-C", self.PROJECT_HOME, "push", remote_url, branch])
            print("Pushing successful")
            return
        print("Pushing not done!")

    def get_project_home(self):
        if self.PROJECT_HOME is None:
            self.PROJECT_HOME = input("Please enter the project directory: ")

    def show_branch_state(self,branch_prefix):
        subprocess.call(["git", "-C", self.PROJECT_HOME,"show-branch","--list",branch_prefix + "-*"])

    def merge_branch(self, branch_from):
        merge_result = subprocess.call(["git","-C", self.PROJECT_HOME,"merge", branch_from])
        if merge_result is 1 :
            exit("Please resolve conflict before continue")

    def get_clean_branch_state(self, branch):
        print("-- Step 1:     Change local repository to " + branch + " --")
        ahead = self.checkout_branch(branch)

        print("-- Step 2:     Show Status of " + branch + " --")
        has_commits = self.has_files_to_commit()
        if has_commits is True:
            self.commit_changes()

        print("-- Step 3:     Pull current version of " + branch + " from GitHub --")
        up_to_date = self.pull_branch(branch)

        if not up_to_date:
            exit("Please check pulled changes and reexecute this script again")

        if ahead is True or has_commits is True:
            self.push_branch(branch)
