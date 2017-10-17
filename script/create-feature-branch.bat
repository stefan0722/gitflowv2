@echo off
setlocal
:: This is a script for the GIT Flow process to create a new feature branch

:: first change to your develop branch
echo Switch local repository to develop branch
git checkout develop
echo ... done

echo Files that should be commited before resuming:
git status -s

:: commit already not commited files to develop branch (OPTIONAL). If not done, the not commited Files
:: will move the feature branch as not commited files
echo Commit all local changes
SET /P confirm="Should the changes be commited [y/n]?"
IF %confirm% == "y" git commit -a

:: push all commited Files to the develop branch
:: make sure that all your changes are on the dev branch
echo Pushing changes to develop branch
SET /P confirm="Should the commited changes be pushed to github [y/n]?"
IF %confirm% == "y" git push origin develop

:: crate new feature branch locally
echo Create new Feature branch locally
SET /P feature_branch_name="Please enter the name of the feature branch [feature-]"
git checkout -b feature-%feature_branch_name% develop

:: increase version on feature branch
echo Increasing version of feature branch
"%M2_HOME%/bin/mvn" release:update-versions

echo Commiting update POM Files
:: commit the pom file with the updated version
git commit -m "changing feature version to new version" *pom.xml
echo ... done

:: publish the feature branch to github, so that everybody sees it
echo Pushing Feature branch to Github
SET /P confirm="Should the feature branch be pushed to gitgub [y/n]"
IF %confirm% == "y" git push origin feature-%feature_branch_name%
endlocal