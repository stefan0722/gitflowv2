@echo off
setlocal
cls
git show-branch --list feature-*
echo .
SET /P feature_branch="Please enter name of feature branch: feature-"
echo.
echo Change to feature branch
git checkout feature-%feature_branch%
echo.
echo.
echo Pull current version from GitHub
git pull origin feature-%feature_branch%
echo.
echo.
echo Status of branch:
git status -s
echo.
echo.
SET /P handwork="Do you need to do some manual merges [y/n]?"
IF "%handwork%" == "y" GOTO exit
echo.
echo.
echo Commiting Changes to local feature branch
git commit -a
echo.
echo.
echo Pushing changes to GitHub
git push origin feature-%feature_branch%
echo.
echo.
echo Change to develop branch
git checkout develop
echo.
echo.
echo Get all changes from Github
git pull origin develop
echo.
echo.
SET /P handwork="Do you need to do some manual merges [y/n]?"
IF "%handwork%" == "y" GOTO exit
echo.
echo.
echo Merge feature-%feature_branch% to develop
git merge --no-ff feature-%feature_branch%
echo.
echo.
echo Delete feature branch locally
git branch -d feature-%feature_branch%
echo.
echo.
echo Increasing version of develop branch
call "%M2_HOME%/bin/mvn" release:update-versions
echo.
echo.
echo Commiting update POM Files
:: commit the pom file with the updated version
git commit -m "changing develop version to new version" *pom.xml
echo.
echo.
echo Push the merge with version change to GitHub
git push origin develop

endlocal

:exit
echo Feature Branch batch job ended