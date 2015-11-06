### Godep使用
### 安装
<pre><code>
go get github.com/tools/godep
</code></pre>
可能碰到如下错误：
<pre><code>
...server certificate verification failed. CAfile: /etc/ssl/certs/ca-certificates.crt CRLfile: none
</code></pre>
原因是主机要求SSL认证。
解决办法是：
<pre><code>
 export GIT_SSL_NO_VERIFY=1
</code></pre>

http://docs.coding.io/languages/go/
### 使用
* 编译
<pre><code>godep go build
</code></pre>
* 更新godep目录下的库
<pre><code>godep restore  //如果GOPATH下没有项目Godep中的库；需要在项目目录下执行
godep get 要更新的库      //git clone 也可以，golang的库由于墙的原因可能更新失败，可以从github获取https://github.com/golang
godep update 要更新的库   //需要在项目目录下执行
</code></pre>
