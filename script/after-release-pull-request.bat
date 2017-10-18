@echo off
setlocal
cls

git show-branch --list release-*
echo.
SET /P release_branch="Please enter version of release branch: release-"
echo.
echo.
echo -- Step 1:    Run Tests on release-%release_branch% branch --
git checkout release-%release_branch%
call "%M2_HOME%/bin/mvn" test
echo.
echo.
echo -- Step 2:       Change local repository to master branch --
git checkout master
echo.
echo.
echo -- Step 3:       Merge release-%release_branch% to master
git merge --no-ff release-%release_branch%
echo.
echo.
echo -- Step 4:       Create Tag from master with name v%release_branch%
git tag -a v%release_branch% -m "Creating Tag for Release %release_branch%"
echo.
echo.
echo -- Step 5:       Push changes to master branch on GitHub
git push origin master
echo -- Step 6:       Push Release Tag v%release_branch% on GitHub
git push origin v%release_branch%
echo.
echo.
echo -- Step 7:       Change local repository to develop branch --
git checkout develop
echo.
echo.
echo -- Step 8:       Merge release-%release_branch% to develop --
git merge --no-ff release-%release_branch%
echo.
echo.
echo -- Step 9:       Update versions of develop branch to next Snapshot version --
call "%M2_HOME%/bin/mvn" versions:set -DnextSnapshot=true -DprocessAllModules=true -DgenerateBackupPoms=false
echo.
echo.
echo -- Step 10:       Delete local release branch --
git branch -d release-%release_branch%
echo.
echo.
echo -- Step 11:       Commit updated pom files to develop branch
:: commit the pom file with the updated version
git commit -m "changing develop version to new version" *pom.xml
echo.
echo.
echo -- Step 12:       Push changes (POM commit) to GitHub
git push origin develop
echo.
echo.
echo -- Step 13:       Change local repository to tag v%release_branch% branch --
git checkout v%release_branch%
echo.
echo.
echo -- Step 14:       Call Maven deploy for deploying the tagged result to artifactory --
SET /P goal="Please enter maven goal to be executed [install|deploy]?"
IF /I "%goal%" == "y" goto error
call "%M2_HOME%/bin/mvn" %goal%
echo.
echo.
echo -- Step 15:       Change local repository to develop branch --
git checkout develop