@echo off
:: This is a script for the GIT Flow process to create a new feature branch

:: first change to your develop branch
echo Switch local repository to develop branch
git checkout develop

:: commit already not commited files to develop branch (OPTIONAL). If not done, the not commited Files
:: will move the feature branch as not commited files
SET /P commit=Sollen alle Änderungen von debelop branch lokal commited werden?
git commit -a

:: push all commited Files to the develop branch
:: make sure that all your changes are on the dev branch
git push origin develop

:: crate new feature branch locally
git checkout -b feature-?? develop

:: increase version on feature branch
"%M2_HOME%/bin/mvn" release:update-versions

:: commit the pom file with the updated version
git commit -m "changing feature version to new version" *pom.xml

:: publish the feature branch to github, so that everybody sees it
git push origin feature-??
