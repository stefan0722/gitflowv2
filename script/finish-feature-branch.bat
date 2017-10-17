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
echo Start Pull Request for Feature to master
git request-pull feature-%feature_branch% origin develop

echo Now Please Go To GitHub and Do a Pull Request on feature-%feature_branch%
echo Or continue with the after-festure-pull-request.bat

endlocal

:exit
echo Feature Branch batch job ended