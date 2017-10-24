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
            success = subprocess.call(["git", "-C", self.PROJECT_HOME, "checkout", complete_branch_name], shell=True)
            self.check_success(success, "Error at checkout of branch")
        return complete_branch_name

    def increase_branch_version(self, is_snapshot=True):
        increase = input("Should the version be increased? [Y/N]: ")
        if increase is "Y":
            version = input("Please enter the new version: ")
            if is_snapshot:
                version = version + "-SNAPSHOT"
            success = subprocess.call([self.M2_HOME + "/bin/mvn", "versions:set",
                         "-f=" + self.PROJECT_HOME,
                         "-DnewVersion=" + version, "-DprocessAllModules=true",
                         "-DgenerateBackupPoms=false"], shell=True)
            self.check_success(success, "Error setting next maven version to " + version)
            return version
        return None

    def increase_branch_version_next_snapshot(self):
        increase = input("Should the version be increased? [Y/N]: ")
        if increase is "Y":
            success = subprocess.call([self.M2_HOME + "/bin/mvn", "versions:set",
                         "-f=" + self.PROJECT_HOME,
                         "-DnextSnapshot=true",
                         "-DprocessAllModules=true",
                         "-DgenerateBackupPoms=false"], shell=True)
            self.check_success(success, "Error setting next maven version!")

    def execute_maven_goal(self, maven_goal):
        success = subprocess.call([self.M2_HOME + "/bin/mvn", maven_goal,
                         "-f=" + self.PROJECT_HOME], shell=True)
        self.check_success(success, "Error executing " + maven_goal + "!")

    def commit_changes(self, message=None, file_pattern=None):
        entry = input("Should the changes be committed to local repository? [Y/N]: ")
        if entry is "Y":
            if message is None:
                message = input("Please enter commit message: ")
            if file_pattern is None:
                success = subprocess.call(["git", "-C", self.PROJECT_HOME, "commit", "-a", "-m", message])
                self.check_success(success, "Error while committing to local repository, please check and try again")
                return
            success = subprocess.call(["git", "-C", self.PROJECT_HOME, "commit", "-m", message, self.PROJECT_HOME +
                                       "/" + file_pattern])
            self.check_success(success, "Error while committing to local repository, please check and try again")

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
            devnull = open(os.devnull, 'w')
            success = subprocess.call(["git", "-C", self.PROJECT_HOME, "push", remote_url, branch], stdout=devnull)
            if success is not 0:
                self.GIT_PASSWORD = None
                exit("Error while pushing to GitHub. Please check username in Git config.name and password")
            print("Pushing successful")
            return
        exit("Please Push to branch in oder to continue!")

    def get_project_home(self):
        if self.PROJECT_HOME is None:
            self.PROJECT_HOME = input("Please enter the project directory: ")

    def show_branch_state(self, branch_prefix):
        subprocess.call(["git", "-C", self.PROJECT_HOME, "show-branch", "--list", branch_prefix + "-*"])

    def merge_branch(self, branch_from):
        merge_result = subprocess.call(["git", "-C", self.PROJECT_HOME, "merge", branch_from])
        self.check_success(merge_result, "Please resolve conflict before continue")

    def merge_branch_no_ff(self, branch_from):
        merge_result = subprocess.call(["git", "-C", self.PROJECT_HOME, "merge", "--no-ff", branch_from])
        self.check_success(merge_result, "Please resolve conflict before continue")

    def delete_branch_locally(self, branch):
        delete_result = subprocess.call(["git", "-C", self.PROJECT_HOME, "branch", "-d", branch])
        self.check_success(delete_result, "An error occured while deleting the branch")

    def get_current_branch_name(self):
        branch_list = subprocess.check_output(["git","-C", self.PROJECT_HOME,"branch","--list"]).decode("utf-8")
        branch_name = None
        for name in branch_list.splitlines() :
            if "* " in name :
                branch_name = name.replace("* ","")
                return branch_name
        return branch_name

    def create_release_tag(self, release_version):
        success = subprocess.call(["git","tag","-a","v" + release_version,
                                   "-m","Creating Tag for Release v" + release_version])
        self.check_success(success,"Error creating a tag")

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

    @staticmethod
    def check_success(exit_code, error_msg):
        if exit_code is not 0:
            exit(error_msg)
