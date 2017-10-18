@echo off
setlocal
cls

git show-branch --list release-*
echo.
SET /P release_branch="Please enter version of release branch: release-"
echo.
echo Change to release branch
git checkout -b release-%release_branch% origin/release-%release_branch%
echo.
echo.
echo Pull current version from GitHub
git pull origin release-%release_branch%
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
echo Commiting Changes to local release branch
git commit -a
echo.
echo.
echo Pushing changes to GitHub
git push origin release-%release_branch%
echo.
echo.

echo Change local branch to master
git checkout master
echo.
echo.
echo Get the latest version of master
git pull origin master
echo.
echo.
echo.
echo "Switch to release workspace"
git checkout release-%release_branch%
echo.
echo.
echo "Merge from master branch to release branch"
git merge master
echo.
echo.
:: echo Start Pull Request for Release to master
:: git request-pull release-%release_branch% origin master

echo Now Please Go To GitHub and Do a Pull Request on release-%release_branch%

endlocal

:exit
echo Feature Branch batch job ended