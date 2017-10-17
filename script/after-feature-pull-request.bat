@echo off
setlocal
cls

git show-branch --list feature-*
echo.
SET /P release_branch="Please enter version of release branch: feature-"
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
call "%M2_HOME%/bin/mvn" versions:set -DnextSnapshot=true
echo.
echo.
echo Commiting update POM Files
:: commit the pom file with the updated version
git commit -m "changing develop version to new version" *pom.xml
echo.
echo.
echo Push the merge with version change to GitHub
git push origin develop