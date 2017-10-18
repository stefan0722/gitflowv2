@echo off
setlocal
cls

git show-branch --list release-*
echo.
SET /P release_branch="Please enter version of release branch: release-"
echo.
echo -- Step 1:     Change local repository to release-%release_branch% branch --
git checkout release-%release_branch%
echo.
echo.
echo -- Step 2:     Pull current version of release-%release_branch% from GitHub --
git pull origin release-%release_branch%
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
echo -- Step 4:     Commiting Changes to local release-%release_branch% --
SET /P handwork="Do you want to commit changes [y/n]?"
IF "%handwork%" == "y" git commit -a
echo.
echo.
echo -- Step 5:     Pushing changes of release-%release_branch% to GitHub --
SET /P handwork="Do you want to push changes [y/n]?"
IF "%handwork%" == "y" git push origin release-%release_branch%
echo.
echo.
echo -- Step 6:     Change local repository to master branch --
git checkout master
echo.
echo.
echo -- Step 7:     Pull current version of master from Github
git pull origin master
echo.
SET /P handwork="Do you need to do some manual merges [y/n]?"
IF "%handwork%" == "y" GOTO exit
echo.
echo.
echo -- Step 8:     Change local repository to release-%release_branch% branch --
git checkout release-%release_branch%
echo.
echo.
echo -- Step 9:     Merge from master branch to release-%release_branch% branch
git merge master
echo.
echo.
:: echo Start Pull Request for Release to master
:: git request-pull release-%release_branch% origin master
echo -- Step 10:    Please resolve conflicts and commit manually (if there are conflicts)!
echo -- Step 11:    Now Please Go To GitHub and Do a Pull Request on release-%release_branch%
echo -- Step 12:    Or continue with the after-release-pull-request.bat

endlocal

:exit
echo Release Branch batch job ended