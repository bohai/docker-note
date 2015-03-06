***先来看来两个命令：***  
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
***docker stop***会向容器发送一个***SIGTERM***信号，然后过一段时间再发送***SIGKILL***信号。   
我们知道，处理良好的程序可以捕捉***SIGTERM***信号，并进行清理动作然后退出。但是也可能可以忽略该信号。  
但是经过***-t（默认10S）***时间后，会再发送***SIGKILL***信号触发进程的最终的退出。    
