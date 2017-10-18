@echo off
setlocal
cls

echo -- Step 1:     Pull current version of develop from GitHub --
git pull origin develop
echo.
echo.
:: first change to your develop branch
echo.
echo.
echo -- Step 2:     Change local repository to develop branch --
git checkout develop
echo.
echo.
SET /P handwork="Do you need to do some manual merges [y/n]?"
IF /I "%handwork%" == "y" goto error
echo.
echo.
echo -- Step 3:     Show Status of branch --
git status -s
echo.
echo.
:: commit already not commited files to develop branch (OPTIONAL). If not done, the not commited Files
:: will move the feature branch as not commited files
echo -- Step 4:     Commit all local changes to develop branch --
SET /P confirm_1="Should the changes be commited [y/n]?"
IF /I "%confirm_1%" == "y" git commit -a

echo.
echo.
:: push all commited Files to the develop branch
:: make sure that all your changes are on the dev branch
echo -- Step 5:     Push changes to develop branch
SET /P confirm_2="Should the commited changes be pushed to github [y/n]?"
IF "%confirm_2%" == "y" git push origin develop

goto exit

:error
echo !Skip Process!
EXIT /B -1

:exit
endlocal