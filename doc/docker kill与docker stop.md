先来看来两个命令：  
<pre><code>
[root@localhost home]# docker kill

Usage: docker kill [OPTIONS] CONTAINER [CONTAINER...]

Kill a running container using SIGKILL or a specified signal

  -s, --signal="KILL"    Signal to send to the container
[root@localhost home]# docker stop

Usage: docker stop [OPTIONS] CONTAINER [CONTAINER...]

Stop a running container by sending SIGTERM and then SIGKILL after a grace period

  -t, --time=10      Number of seconds to wait for the container to stop before killing it. Default is 10 seconds.
</code></pre>
