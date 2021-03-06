#!/usr/bin/python

import subprocess
import getpass
import os
import platform
import xml.etree.ElementTree as et


class GitFunctions:
    PROJECT_HOME = None
    GIT_USER_NAME = None
    M2_HOME = os.environ.get("M2_HOME")
    GIT_PASSWORD = None
    VERSION_PROPERTY = None
    REPOSITORY_ID = None
    RELEASE_REPOSITORY_URL = None
    SNAPSHOT_REPOSITORY_URL = None

    def __init__(self):
        self.load_environment_var()
        self.get_project_home()

    def load_environment_var(self):
        with open("environment.txt", "r") as f:
            for line in f.read().splitlines():
                if line.startswith("#"):
                    continue
                elements = line.split('=')
                key = elements[0]
                value = elements[1]
                if key is "M2_HOME":
                    self.M2_HOME = value
                if "PROJECT_HOME" in key:
                    self.PROJECT_HOME = value
                if "GIT_USER_NAME" in key:
                    self.GIT_USER_NAME = value
                if "VERSION_PROPERTY" in key:
                    self.VERSION_PROPERTY = value
                if "REPOSITORY_ID" in key:
                    self.REPOSITORY_ID = value
                if "RELEASE_REPOSITORY_URL" in key:
                    self.RELEASE_REPOSITORY_URL = value
                if "SNAPSHOT_REPOSITORY_URL" in key:
                    self.SNAPSHOT_REPOSITORY_URL = value

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

    def increase_branch_version(self, is_snapshot=True, version=None):
        if version is None:
            increase = input("Should the version be increased? [Y/N]: ")
            if increase.lower() == "Y".lower():
                return self.__call_increase_version__(version, is_snapshot)
        else:
            return self.__call_increase_version__(version, is_snapshot)

    def increase_feature_branch_version(self, is_snapshot=True):
        version = input("New version of feature branch: ")
        if version is None:
            increase = input("Should the version be increased? [Y/N]: ")
            if increase.lower() == "Y".lower():
                return self.__call_increase_version__(version, is_snapshot)
        else:
            return self.__call_increase_version__(version, is_snapshot)

    def __call_increase_version__(self, version, is_snapshot):
        if is_snapshot:
            version = version + "-SNAPSHOT"

        mvn_path = self.norm_path(self.M2_HOME + "/bin/mvn")
        mvn_cmd = ''.join([mvn_path + " versions:set -f=", self.PROJECT_HOME,
        	" -DnewVersion=", version, " -DprocessAllModules=true -DgenerateBackupPoms=false" ])
        print("executing maven command: " + mvn_cmd + "\n")
        success = subprocess.call(mvn_cmd, shell=True)
        
        self.check_success(success, "Error setting next maven version to " + version)
        if self.VERSION_PROPERTY is not None:
            self.replace_property_in_pom(self.VERSION_PROPERTY, version)
        return version
        
    def norm_path(self, path):
        normed_path = os.path.normpath(path)
        if platform.system() == "Windows":
            normed_path = "\"" + normed_path + "\""
        return normed_path

    def increase_branch_version_next_snapshot(self):
        increase = input("Should the version be increased? [Y/N]: ")
        if increase.lower() == "Y".lower():
            mvn_path = self.norm_path(self.M2_HOME + "/bin/mvn")
            mvn_cmd = ''.join([mvn_path + " versions:set -f=", self.PROJECT_HOME,
                   " -DnextSnapshot=true -DprocessAllModules=true -DgenerateBackupPoms=false" ])
            print("executing maven command: " + mvn_cmd + "\n")
            success = subprocess.call(mvn_cmd, shell=True)
            self.check_success(success, "Error setting next maven version!")
            if self.VERSION_PROPERTY is not None:
                project_version = self.get_project_version()
                self.replace_property_in_pom(self.VERSION_PROPERTY, project_version)
        return increase.lower() == "Y".lower()

    def execute_maven_goal(self, maven_goal):
        if maven_goal is "deploy":
            self.maven_deploy()
        else:
            mvn_path = self.norm_path(self.M2_HOME + "/bin/mvn")
            mvn_cmd = ''.join([mvn_path, " ", maven_goal, " -f=", self.PROJECT_HOME])
            print("executing maven command: " + mvn_cmd + "\n")
            success = subprocess.call(mvn_cmd, shell=True)
            self.check_success(success, "Error executing " + maven_goal + "!")

    def maven_deploy(self):
        project_version = self.get_project_version()
        if "SNAPSHOT" in str(project_version):
            if self.SNAPSHOT_REPOSITORY_URL is None:
                repository_url = input("Please enter snapshot repository server url (e.g. "
                                       "http://localhost/artifactory/libs-snapshot-local): ")
            else:
                repository_url = self.SNAPSHOT_REPOSITORY_URL
        else:
            if self.RELEASE_REPOSITORY_URL is None:
                repository_url = input("Please enter repository server url (e.g. "
                                       "http://localhost/artifactory/libs-release-local): ")
            else:
                repository_url = self.RELEASE_REPOSITORY_URL
        if self.REPOSITORY_ID is None:
            self.REPOSITORY_ID = input("Please enter repository ID (e.g. Artifactory Server): ")
        mvn_path = self.norm_path(self.M2_HOME + "/bin/mvn")
        mvn_cmd = ''.join([mvn_path + " deploy -f=", self.PROJECT_HOME,
                 " -DaltDeploymentRepository=", self.REPOSITORY_ID, "::default::", repository_url])
        print("executing maven command: " + mvn_cmd + "\n")
        success = subprocess.call(mvn_cmd, shell=True)
        self.check_success(success, "Error executing deploy !")

    def commit_changes(self, message=None, file_pattern=None):
        entry = input("Should the changes be committed to local repository? [Y/N]: ")
        if entry.lower() == "Y".lower():
            if message is None:
                message = input("Please enter commit message: ")
            if file_pattern is None:
                success = subprocess.call(["git", "-C", self.PROJECT_HOME, "commit", "-a", "-m", message])
                self.check_success(success, "Error while committing to local repository, please check and try again")
                return
            success = subprocess.call(["git", "-C", self.PROJECT_HOME, "commit", "-m", message, self.PROJECT_HOME +
                                       "/" + file_pattern])
            self.check_success(success, "Error while committing to local repository, please check and try again")
        return entry.lower() == "Y".lower()

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
        if "Already up-to-date" in text or "Already up to date" in text:
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
        if entry.lower() == "Y".lower():
            remote_url = GitFunctions.get_remote_url(self)
            username = GitFunctions.get_username(self)
            if self.GIT_PASSWORD is None:
                self.GIT_PASSWORD = getpass.getpass("Please enter password for " + remote_url + ": ")
            remote_url = remote_url.replace("https://github.com/",
                                            "https://" + username + ":" + self.GIT_PASSWORD + "@github.com/")
            devnull = open(os.devnull, 'w')
            success = subprocess.call(["git", "-C", self.PROJECT_HOME, "push", remote_url, branch],
                                      stdout=devnull, stderr=devnull)
            if success is not 0:
                self.GIT_PASSWORD = None
                exit("Error while pushing to GitHub. Please check username in Git config.name and password")
            print("Pushing successful")
            return True
        exit("Please Push to branch in order to continue!")

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
        branch_list = subprocess.check_output(["git", "-C", self.PROJECT_HOME, "branch", "--list"]).decode("utf-8")
        branch_name = None
        for name in branch_list.splitlines():
            if "* " in name:
                branch_name = name.replace("* ", "")
                return branch_name
        return branch_name

    def create_release_tag(self, release_version):
        subprocess.call(["git", "-C", self.PROJECT_HOME, "tag", "-a", "v" + release_version,
                         "-m", "Creating Tag for Release v" + release_version])

    def reset_commits(self, number_of_commits=1):
        success = subprocess.call(["git", "-C", self.PROJECT_HOME, "reset", "--soft", "HEAD~" + str(number_of_commits)])
        self.check_success(success, "Error reset last commit")

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

    def get_project_version(self):
        return et.parse(self.PROJECT_HOME + "/pom.xml").find('{http://maven.apache.org/POM/4.0.0}version').text

    def replace_property_in_pom(self, tag_name, new_value):
        tree = et.parse(self.PROJECT_HOME + "/pom.xml")
        tag = tree.find(".//{http://maven.apache.org/POM/4.0.0}" + tag_name)
        if tag is None:
            exit("No Tag found in POM : " + tag_name)
        tag.text = new_value
        tree.write(self.PROJECT_HOME + "/pom.xml",
                   default_namespace='http://maven.apache.org/POM/4.0.0')
        print("\n Tag " + tag_name + " set to " + new_value)

    @staticmethod
    def check_success(exit_code, error_msg):
        if exit_code is not 0:
            exit(error_msg)
