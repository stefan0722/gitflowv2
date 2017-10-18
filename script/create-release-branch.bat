@echo off
setlocal

call script\before-branch.bat

echo.
echo.
:: crate new feature branch locally
echo -- Step 6:     Create new Release branch locally
SET /P release_version="Please enter the release version:"
git checkout -b release-%release_version% develop

echo.
echo.
:: increase version on feature branch
echo -- Step 7:     Set version in POM to %release_version%
call "%M2_HOME%/bin/mvn" versions:set -DnewVersion=%release_version% -DprocessAllModules=true -DgenerateBackupPoms=false

echo.
echo.
echo -- Step 8:     Commiting update POM Files to release-%release_version%
:: commit the pom file with the updated version
git commit -m "changing release version to %release_version%" *pom.xml
echo ... done

echo.
echo.
:: publish the feature branch to github, so that everybody sees it
echo -- Step 9:     Pushing release-%release_version% branch to Github
SET /P confirm="Should the release-%release_version% be pushed to gitgub [y/n]"
IF "%confirm%" == "y" git push origin release-%release_version%
endlocal

:exit
echo Release Branch batch job ended
