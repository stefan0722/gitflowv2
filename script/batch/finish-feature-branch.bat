@echo off
setlocal
cls
git show-branch --list feature-*
echo .
SET /P feature_branch="Please enter name of feature branch: feature-"
echo.
echo -- Step 1:     Change local repository to feature-%feature_branch% branch --
git checkout feature-%feature_branch%
echo.
echo.
echo -- Step 2:     Pull current version of feature-%feature_branch% from GitHub --
git pull origin feature-%feature_branch%
echo.
echo.
echo -- Step 3:     Show Status of branch --
git status -s
echo.
echo.
SET /P handwork="Do you need to do some manual merges [y/n]?"
IF "%handwork%" == "y" GOTO exit
echo.
echo.
echo -- Step 4:     Commiting Changes to local feature-%feature_branch% --
SET /P handwork="Do you want to commit changes [y/n]?"
IF "%handwork%" == "y" git commit -a
echo.
echo.
echo -- Step 5:     Pushing changes of feature-%feature_branch% to GitHub --
SET /P handwork="Do you want to push changes [y/n]?"
IF "%handwork%" == "y" git push origin feature-%feature_branch%
echo.
echo.
echo -- Step 6:     Change local repository to develop branch --
git checkout develop
echo.
echo.
echo -- Step 7:     Pull current version of develop from Github
git pull origin develop
echo.
echo.
SET /P handwork="Do you need to do some manual merges [y/n]?"
IF "%handwork%" == "y" GOTO exit
echo.
echo.
echo -- Step 8:     Push uncommited changes to develop branch
git push origin develop
echo.
echo.
echo -- Step 9:     Change local repository to feature-%feature_branch% branch --
git checkout feature-%feature_branch%
echo.
echo.
echo -- Step 10:    Merge from develop branch to feature-%feature_branch% branch
git merge develop
echo.
echo.
echo -- Step 11:    Please resolve conflicts and commit manually (if there are conflicts)!
echo -- Step 12:    Now Please Go To GitHub and Do a Pull Request on feature-%feature_branch%
echo -- Step 13:    Or continue with the after-festure-pull-request.bat

endlocal

:exit
echo Feature Branch batch job ended