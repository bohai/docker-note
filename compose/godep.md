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
