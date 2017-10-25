# gitflowv2

Test project with (transparent) python scripts for the [GitFlow](https://datasift.github.io/gitflow/IntroducingGitFlow.html) workflow.
The python scripts are meant to be for Java projects build with Apache Maven. An [example
Java project](/src) is also present in this folder.
The script offers the user exactly all information what steps are executed and interacts on command line level. This is the main
difference from all other git flow tools. 

## Setup

All properties are stored in [environment.txt](script/python/environment.txt). Some example properties have been included
for better understanding. The complete List of possible properties are:

| key  | example value | description |
| :--- | :---- | :---- |
| PROJECT_HOME | /usr/home/gitflowv2 | java project root folder with base pom file and .git folder |
| GIT_USER_NAME | anonymous | Username used for Git |
| VERSION_PROPERTY |  subproject.version | additional project version stored as maven property |
| REPOSITORY_ID | artifactory | ID of repository like stored in the settings.xml of maven |
| RELEASE_REPOSITORY_URL | https://artifactory/libs-release-local | Maven repository URL for releases |
| SNAPSHOT_REPOSITORY_URL | https://artifactory/libs-snapshot-local | Maven repository URL for snapshots |

## What does gitflowv2 ?

It provides python scripts for creating and finishing, feature and release branches as well as a default push mechanism

### Development
During development the commits should be pushed to github. This could be done by the [push-script](script/python/p01_standard-push.py):
* Checks if there are any staged files and asks to **commit** them
* **Pulls** changes from origin (GitHub)
* **Increases project version** to next SNAPSHOT version
* **Commits** changed maven **pom.xml** files
* Executes a **maven deploy** and publishes the artifact to the repository server
* **Pushes** all commits to origin (GitHub)

### Feature
#### Create
When working on a new feature, an own feature branch should be created from the develop branch. Therefore
the [create-feature-script](script/python/f01_create-feature-branch.py) can be used:
* Cleans up develop branch
    * **Checkout** develop branch
    * **Commit** staged changes
    * **Pull** HEAD from origin (GitHub)
    * Resolve conficts manually (if there are any)
    * **Push** commits to origin (GitHub)
* **Checkout** new feature branch (local repository)
* Set feature branch **version** (user prompt)
* **Commit** changed maven pom.xml(s)
* **Push** new branch to origin (GitHub)

#### Finish
After having finished the feature it should be merged back to develop branch. This is done in two steps.
First a clean state of develop and feature branch is checked out and a pull request is created. This is done by the
[finish-feature-branch-script](/script/python/f02_finish-feature-branch.py):
* Cleans up feature branch
    * **Checkout** feature branch
    * **Commit** staged changes    
    * **Pull** HEAD from origin (GitHub)
    * Resolve conficts manually (if there are any)
    * **Push** commits to origin (GitHub)
* Cleans up develop branch
    * **Checkout** develop branch
    * **Commit** staged changes    
    * **Pull** HEAD from origin (GitHub)
    * Resolve conficts manually (if there are any)
    * **Push** commits to origin (GitHub)
* **Merge** develop branch to feature branch
* Resolve conflicts manually
* **Push** changes to GitHub
* Open webbrowser on GitHub page to create a Pull Request

#### Merge
After the pull request has been reviewed (optional) the merge will be executed and the  pull request resolved.
This is done by the [after-feature-pull-request-script](script/python/f03_after-feature-pull-request.py):
* Cleans up feature branch
    * **Checkout** feature branch
    * **Commit** staged changes    
    * **Pull** HEAD from origin (GitHub)
    * Resolve conficts manually (if there are any)
    * **Push** commits to origin (GitHub)
* Executes **maven test**s on feature branch
* Cleans up develop branch
    * **Checkout** develop branch
    * **Commit** staged changes    
    * **Pull** HEAD from origin (GitHub)
    * Resolve conficts manually (if there are any)
    * **Push** commits to origin (GitHub)
* **Merge** feature branch into develop with fastforward excluded
* **Delete** local feature branch
* Increase maven project **version** in develop branch
* **Commit** changed maven pom.xml to develop branch
* **Push** changes to origin (GitHub)  

### Release
#### Create
When preparing a new release, an own release branch should be created from the develop branch. Therefore
the [create-release-script](script/python/r01_create-release-branch.py) can be used:
* Cleans up develop branch
    * **Checkout** develop branch
    * **Commit** staged changes
    * **Pull** HEAD from origin (GitHub)
    * Resolve conficts manually (if there are any)
    * **Push** commits to origin (GitHub)
* **Checkout** new release branch (local repository)
* Set release branch **version** to a non-SNAPSHOT version (user prompt)
* **Commit** changed maven pom.xml(s)
* **Push** new release branch to origin (GitHub)

### Finish
After having adapted small changes to the release the release process could be started. In a first step, a pull
request is created with the [finish-release-branch-script](script/python/r02_finish-release-branch.py):
* Cleans up release branch
    * **Checkout** feature branch
    * **Commit** staged changes    
    * **Pull** HEAD from origin (GitHub)
    * Resolve conficts manually (if there are any)
    * **Push** commits to origin (GitHub)
* **Checkout** master branch
* **Pull** HEAD of master branch from origin (GitHub)
* **Merge** master branch to release branch
* Resolve conflicts manually
* **Push** changes on release branch to GitHub
* Open webbrowser on GitHub page to create a Pull Request

### Release, Tag, Merge, Deploy
Finally the release branch should be released. This means it should be merged to master, tagged and brought back into
develop branch. Finally the result should be deployed to the repository server
* **Checkout** release branch
* Execute **maven test** goal
* **Checkout** master branch
* **Merge** release branch to master branch (without fastforward)
* Create release **tag** from master
* **Push** changes to origin (master and tag)
* Clean up develop branch
    * **Checkout** develop branch
    * **Commit** staged changes
    * **Pull** HEAD from origin (GitHub)
    * Resolve conficts manually (if there are any)
    * **Push** commits to origin (GitHub)
* **Merge** release branch to develop branch (without fastforward)
* Increase **version** of develop branch to next snapshot version
* **Commit** changes of maven pom.xml to origin (GitHub)
* **Delete** Release branch locally
* **Push** commits of branch develop to origin
* **Checkout** tag (warning because it is behind HEAD)
* Execute **maven deploy** and deploy the artifact on repository server
* **Checkout** branch develop


## Requirements

* Python 3
* Maven 3
* Maven Versions Plugin 2.5
* Repository (e.g. on GitHub) with **master** and **develop** branch

  
