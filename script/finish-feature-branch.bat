@echo off
setlocal

::this script merges the feature branch back to develop
git checkout feature-??

git status -s

git commit -a

git publish origin feature-??

