libcompose compile
----
0. expport GOPATH="your work directory"
1. go get github.com/docker/libcompose
2. cd $GOPATH/src/github.com/docker/libcompose/
3. export GOPATH=`godep path`:$GOPATH
4. cd cli/main/
5. go build
6. ./main



精简版
----
0. export GOPATH="your work directory":"your libcompose GODEP directory" 
<pre><code>举例：
GOPATH=/home/temp/go/src/github.com/docker/libcompose/Godeps/_workspace/:/home/temp/go/</code></pre>
1. cd cli/main/  
2. go build  


gdb debug
----
关闭编译优化。
<pre><code>go build -gcflags "-N -l"</code></pre>



