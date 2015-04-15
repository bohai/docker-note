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

使用docker运行应用，你也许会用到信号，来和容器重的应用通信，比如重载配置，在程序结束时清理，进行协调等。

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
![image](https://d262ilb51hltx0.cloudfront.net/max/795/1*ZAZWGqxfJh59DsqQlFWakw.png)
  
