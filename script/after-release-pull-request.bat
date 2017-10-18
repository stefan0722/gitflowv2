@echo off
setlocal
cls

git show-branch --list release-*
echo.
SET /P release_branch="Please enter version of release branch: release-"
echo.
echo.
echo Change local branch to master
git checkout master
echo.
echo.
echo Merge release branch to master
git merge --no-ff release-%release_branch%
echo.
echo.
echo Create a tag of this version on master branch
git tag -a v%release_branch% -m "Creating Tag for Release %release_branch%"
echo.
echo.
echo Push changes to master and push tag
git push origin master
git push origin v%release_branch%
echo.
echo.
echo Change to develop workspace
git checkout develop
echo.
echo.
echo Merge changs from release branch
git merge --no-ff release-%release_branch%
echo.
echo.
echo Update Versions
call "%M2_HOME%/bin/mvn" versions:set -DnextSnapshot=true -DprocessAllModules=true
echo.
echo.
echo Delete the local release branch
git branch -d release-%release_branch%
echo.
echo.
echo Commiting update POM Files
:: commit the pom file with the updated version
git commit -m "changing develop version to new version" *pom.xml
echo.
echo.
echo Push the merge with version change to GitHub
git push origin develop
echo.
echo.
echo Changing to Master repository
git checkout v%release_branch%
echo.
echo.
echo Deploy new master version
call "%M2_HOME%/bin/mvn" deploy
echo.
echo.
echo Finally Change back to develop workspace
git checkout develop