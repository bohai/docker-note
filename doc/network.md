..  
声明：   
本博客欢迎转发，但请保留原作者信息!   
博客地址：http://blog.csdn.net/halcyonbaby   
新浪微博：[@寻觅神迹]( www.weibo.com/u/2230330930)

内容系本人学习、研究和总结，如有雷同，实属荣幸！   

-----
# Docker1.9后的network
### 介绍与使用
1.9之后，在Docker中network从实验特性转为正式特性发布。   
从命令行可以看到新增如下命令：
<pre><code>[root@localhost system]# docker help network

Usage:  docker network [OPTIONS] COMMAND [OPTIONS]

Commands:
  create                   Create a network
  connect                  Connect container to a network
  disconnect               Disconnect container from a network
  inspect                  Display detailed network information
  ls                       List all networks
  rm                       Remove a network

Run 'docker network COMMAND --help' for more information on a command.

  --help=false       Print usage
</code></pre>
可以看到Docker daemon启动后默认创建了3个网络：
分别使用了bridge、null、host三种driver。
<pre><code>[root@localhost system]# docker network ls
NETWORK ID          NAME                DRIVER
f280d6a13422        bridge              bridge
f5d11bed22a2        none                null
18642f53648f        host                host
</code></pre>



### driver实现
### libnetwork与docker


