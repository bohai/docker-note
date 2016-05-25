### download godep 

go get -u github.com/tools/godep

### save dependency (enter the project path)
godep save ./...
git add -A
git commit -m "vendoring dependency"

### load the dependency
godep restore
