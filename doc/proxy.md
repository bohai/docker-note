###解决proxy后docker pull镜像的问题

/etc/sysconfig/docker

Adding below line helped me to get docker daemon working behind proxy server:

export HTTP_PROXY="http://<proxy_host>:<proxy_port>"   
export HTTPS_PROXY="http://<proxy_host>:<proxy_port>"   

###举例 
<pre><code>
# /etc/sysconfig/docker
#OPTIONS="-H unix:///var/run/docker.sock --dns 186.100.4.120"
#http_proxy="http://186.100.4.120:8080"
#https_proxy="http://186.100.4.120:8080"
</code></pre>
