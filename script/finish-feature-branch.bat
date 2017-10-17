@echo off
setlocal

git show-branch --list feature-*
echo .
SET /P feature_branch="Please enter name of feature branch [feature-]"

echo Change to feature branch
git checkout feature-%feature_branch%

echo Pull current version from GitHub
git pull origin feature-%feature_branch%

echo Status of branch:
git status -s

SET /P handwork="Do you need to do some manual merges [y/n]?"
IF %handwork% == "y" GOTO :exit

echo Commiting Changes to local feature branch
git commit -a

echo Pushing changes to GitHub
git push origin feature-%feature_branch%

echo Change to develop branch
git checkout develop

echo Get all changes from Github
git pull origin develop

echo Increasing version of develop branch
"%M2_HOME%/bin/mvn" release:update-versions

echo Commiting update POM Files
:: commit the pom file with the updated version
git commit -m "changing develop version to new version" *pom.xml
echo ... done

endlocal

echo Feature Branch batch job ended
:exit