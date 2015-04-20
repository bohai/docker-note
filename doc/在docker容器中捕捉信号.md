..  
声明：   
本博客欢迎转发，但请保留原作者信息!   
博客地址：http://blog.csdn.net/halcyonbaby   
新浪微博：寻觅神迹

内容系本人学习、研究和总结，如有雷同，实属荣幸！   

==================
(译文）在docker容器中捕捉信号
原文地址： https://medium.com/@gchudnov/trapping-signals-in-docker-containers-7a57fdda7d86

你是否停止过docker容器？  

通常我们可以使用'docker stop'或者'docker kill'停止容器。  
‘docker stop’会先向容器发送SIGTERM信号，容器重的主进程会处理它，在一段时间后，发送SIGKILL结束应用。 

使用docker运行应用，你也许会用到信号，来和容器中的应用通信，比如重载配置，在程序结束时清理，进行协调等。

那么让我们看下，在Docker环境下信号有哪些作用？  

信号
=================
信号是一种进程间通信方式。有kernel通知进程，某些状况的发生。
当信号发送给进程，进程会中断，信号处理函数会被执行。如果没有信号处理函数，默认的处理函数会被调用。
进程可以告诉kernel，自己感兴趣的信号。并注册信号处理函数。  
当你在终端使用'kill'命令，你在请求内核向另一个进程发送信号。  
SIGTERM是一个常见的信号，用来告诉进程关闭并停止。通常用来进行socket关闭，数据连接关闭，删除临时文件等操作。  
许多daemon进程，接受SIGHUP信号，来重载配置文件。  
SIGUSR1和SIGUSR2是用户定义信号，可以由应用自由使用。   
举个node.js中的SIGTERM例子：  
<pre><code>
process.on('SIGTERM', function() {
  console.log('shutting down...');
});
</code></pre>

SIGTERM处理的顺序是，进程会中断执行，先进行信号的处理，然后返回到中断前继续执行。  
通常的信号有：  
![signal] (https://d262ilb51hltx0.cloudfront.net/max/795/1*ZAZWGqxfJh59DsqQlFWakw.png)

除了SIGKILL/SIGSTOP，其他信号处理都可以被再次中断。  

Docker中的信号
===================
'docker kill'用于向docker中的主进程发送信号。  
<pre><code>
Usage: docker kill [OPTIONS] CONTAINER [CONTAINER...]

Kill a running container using SIGKILL or a specified signal

  -s, --signal="KILL"    Signal to send to the container
</code></pre>

发送到docker容器的信号，会被pid=1的主进程处理。  
进程可以忽略信号，也可以使用默认处理或者定义自己的处理函数。  
下面这个例子展示了在容器中运行（program.js)验证信号处理。
<pre><code>
'use strict';
var http = require('http');
var server = http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('Hello World\n');
}).listen(3000, '0.0.0.0');
console.log('server started');
var signals = {
  'SIGINT': 2,
  'SIGTERM': 15
};
function shutdown(signal, value) {
  server.close(function () {
    console.log('server stopped by ' + signal);
    process.exit(128 + value);
  });
}
Object.keys(signals).forEach(function (signal) {
  process.on(signal, function () {
    shutdown(signal, signals[signal]);
  });
});
</code></pre>

我们创建了一个HTTP-server监听3000端口，并设置了两个信号处理来处理SIGINT和SIGTERM。
当信号接收到时，会打印'server stopped by [SIGNAL]'.

应用时主进程(pid=1)的场景
===================
当应用时容器内的主进程（PID1），它可以直接处理信号。

这个Dockerfile用来构建基于io.js的镜像。
<pre><code>
FROM iojs:onbuild

COPY ./program.js ./program.js
COPY ./package.json ./package.json

EXPOSE 3000

ENTRYPOINT ["node", "program"]
</code></pre>

>在编写Dockerfile时，要确保使用ENTRYPOINT或者RUN启动应用。否则的话，应用作为/bin/sh -c的子进程进行启动，而sh是不处理信号的。
>PID为1的进程是shell，你的应用时不会受到任何来自'docker kill'命令的信号。

构建镜像：
<pre><code>
$ docker build -t signal-fg-app .
</code></pre>

运行容器：
<pre><code>
$ docker run -it --rm -p 3000:3000 --name="signal-fg-app" signal-fg-app
</code></pre>

访问http://localhost:3000来确认应用已经运行。 
打开一个新的terminal，并运行命令'docker kill'：
<pre><code>
$ docker kill --signal="SIGTERM" signal-fg-app
</code></pre>
or
<pre><code>
$ docker stop signal-fg-app
</code></pre>
两个命令都用来发送SIGTERM信号，停止应用。 
<pre><code>
server stopped by SIGTERM
</code></pre>

应用不是主进程（pid不是1）
=========================
进程如果不是主进程，则不能直接发送信号。这种情况，一个解决办法是在entrypoint设置处理的shell脚本。  
在shell脚本中处理信号。

Dockerfile的例子：  
<pre><code>
FROM iojs:onbuild

COPY ./program.js ./program.js
COPY ./program.sh ./program.sh
COPY ./package.json ./package.json

RUN  chmod +x ./program.sh

EXPOSE 3000

ENTRYPOINT ["./program.sh"]
</code></pre>
entrypoint中设置的program.sh处理信号：
<pre><code>
#!/usr/bin/env bash
set -x

pid=0

# SIGUSR1-handler
my_handler() {
  echo "my_handler"
}

# SIGTERM-handler
term_handler() {
  if [ $pid -ne 0 ]; then
    kill -SIGTERM "$pid"
    wait "$pid"
  fi
  exit 143; # 128 + 15 -- SIGTERM
}

# setup handlers
# on callback, kill the last background process, which is `tail -f /dev/null` and execute the specified handler
trap 'kill ${!}; my_handler' SIGUSR1
trap 'kill ${!}; term_handler' SIGTERM

# run application
node program &
pid="$!"

# wait indefinetely
while true
do
  tail -f /dev/null & wait ${!}
done
</code></pre>

程序中我们设置了两个信号处理函数。一个用户定义信号SIGUSR1，一个处理SIGTERM从而优雅关闭应用。

脚本中，我们使用&将程序后台运行。 
最终我们使用'wait'来暂停执行一直到子进程退出。当signal信号来临时，'wait'和'waitpid'会被中断。  
当信号来临时，使用指定的函数进行处理然后继续等待下一个信号。  

>按照docker文档，SIGCHLD、SIGKILL、SIGSTOP不会被proxy。  
运行下边的代码，打开一个终端窗口并构建容器镜像：  
<pre><code>
docker build -t signal-bg-app .
</code></pre>

运行容器:  
<pre><code>
docker run -it --rm -p 3000:3000 --name="signal-bg-app" signal-bg-app
</code></pre>

打开一个terminal，发送SIGUSR1：  
<pre><code>
docker kill --signal="SIGUSR1" signal-bg-app
</code></pre>

最后，停止应用：  
<pre><code>
docker kill --signal="SIGTERM" signal-bg-app
</code></pre>

应用会优雅的停止，并在stdout打印对应信息。  

归纳
=========================  
信号提供给了一种处理异步事件的能力。DOcker容器中的应用也可以使用。可以从Host上与容器内应用通信，进行配置重载，清理，多进程间的对齐。   

参考
=========================
1. http://man7.org/linux/man-pages/man7/signal.7.html
2. Michael Kerrisk (2010), The Linux Programming Interface: A Linux and UNIX System Programming Handbook. No Starch Press
