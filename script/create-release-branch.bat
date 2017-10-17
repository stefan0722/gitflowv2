@echo off
setlocal

call script\before-branch.bat

echo.
echo.
:: crate new feature branch locally
echo Create new Release branch locally
SET /P release_version="Please enter the release version:"
git checkout -b release-%release_version% develop

echo.
echo.
:: increase version on feature branch
echo Increasing version of release branch to %release_version%
call "%M2_HOME%/bin/mvn" release:update-versions -DautoVersionSubmodules=true

echo.
echo.
echo Commiting update POM Files
:: commit the pom file with the updated version
git commit -m "changing release version to %release_version%" *pom.xml
echo ... done

echo.
echo.
:: publish the feature branch to github, so that everybody sees it
echo Pushing Release branch to Github
SET /P confirm="Should the release branch be pushed to gitgub [y/n]"
IF "%confirm%" == "y" git push origin release-%release_version%
endlocal

:exit
echo Release Branch batch job ended
