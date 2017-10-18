@echo off
setlocal
cls

git fetch origin
git show-branch --list feature-*
echo.
SET /P feature_branch="Please enter version of feature branch: feature-"
echo.
echo.
echo -- Step 1:    Run Tests on feature-%feature_branch% branch --
git checkout feature-%feature_branch%
call "%M2_HOME%/bin/mvn" test
echo.
echo.
echo -- Step 2:       Change local repository to develop branch --
git checkout develop
echo.
echo.
echo -- Step 3:       Merge feature-%feature_branch% to develop
git merge --no-ff feature-%feature_branch%
echo.
echo.
echo -- Step 4:       Delete feature-%feature_branch% branch locally
git branch -d feature-%feature_branch%
echo.
echo.
echo -- Step 5:       Increasing version of develop branch
call "%M2_HOME%/bin/mvn" versions:set -DnextSnapshot=true -DgenerateBackupPoms=false
echo.
echo.
echo -- Step 6:       Commiting update POM Files to develop branch
:: commit the pom file with the updated version
git commit -m "changing develop version to new version" *pom.xml
echo.
echo.
echo -- Step 7:       Push the merge with version change to GitHub
git push origin develop
