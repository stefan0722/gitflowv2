@echo off
setlocal

call script\before-branch.bat

echo.
echo.
:: crate new feature branch locally
echo -- Step 6:     Create new Feature branch locally
SET /P feature_branch_name="Please enter the name of the feature branch: feature-"
SET /P feature_version="Please enter the version of the feature:"
git checkout -b feature-%feature_branch_name% develop

echo.
echo.
:: increase version on feature branch
echo -- Step 7:     Increasing version of feature-%feature_branch_name% to %feature_version%-SNAPSHOT
call "%M2_HOME%/bin/mvn" versions:set -DnewVersion=%feature_version%-SNAPSHOT -DprocessAllModules=true -DgenerateBackupPoms=false

echo.
echo.
echo -- Step 8:     Commiting update POM Files
:: commit the pom file with the updated version
git commit -m "changing feature version to new version" *pom.xml
echo ... done

echo.
echo.
:: publish the feature branch to github, so that everybody sees it
echo -- Step 9:     Pushing feature-%feature_branch_name% to Github
SET /P confirm="Should the feature branch be pushed to gitgub [y/n]"
IF "%confirm%" == "y" git push origin feature-%feature_branch_name%
endlocal

:exit
echo Feature Branch batch job ended
