### libcompose compile
0. expport GOPATH="your work directory"
1. go get github.com/docker/libcompose
2. cd $GOPATH/src/github.com/docker/libcompose/
3. export GOPATH=`godep path`:$GOPATH
4. cd cli/main/
5. go build
6. ./main
