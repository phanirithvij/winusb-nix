# TODO
# scoop can't be installed via admin pwsh
# will use choco for python
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression

env:$USERPROFILE\scoop\bin\scoop install git
env:$USERPROFILE\scoop\bin\scoop update
