<pre><code>
$ docker pull samalba/docker-registry
$ docker run -d -p 5000:5000 samalba/docker-registry
# 我们先pull下来一个简单的镜像（或者自己做一个也可以）
$ docker pull busybox
$ docker tag busybox localhost:5000/busybox
$ docker push localhost:5000/busybox
</code></pre>
