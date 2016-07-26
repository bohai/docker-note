..  
声明：   
本博客欢迎转发，但请保留原作者信息!   
博客地址：http://blog.csdn.net/halcyonbaby   
新浪微博：@寻觅神迹  
原文地址： https://sreeninet.wordpress.com/2016/07/14/comparing-swarm-swarmkit-and-swarm-mode/

本文系个人翻译，错漏之处请见谅。  

====================================
Swarm、SwarmKit、Swarm mode 对比
====================================
Docker1.12的一个重大特性是提供了swarm mode。Docker结合swarm从1.6开始支持容器编排。  
Docker1.12发布前几周，docker还开源了swarmkit，一个用于编排分布式系统的项目。   
这三个项目让人颇为困惑，这篇博客中我和大家一起看下他们的相似之处以及区别。    
我还会拿一个应用作为例子，来比较三者哪个更容易使用。  

Docker swarm mode和swarm存在本质区别，但是却使用了swarm这个易于混淆的名字。  
我觉得docker社区应该考虑换个名字。另外一点同样增加了这个混淆，native swarm会在1.12继续支持，从而提供兼容性。   
这篇Blog中，我们使用“Swarm”表示老的swarm项目，“Swarmkit”表示新开源的swarmkit项目，“SwarmNext”表示docker swarm mode。   

### Swarm, SwarmNext and Swarmkit  
下边是Swarm和SwarmNext的对比：  

Swarm |SwarmNext
---------|----------
Separate from Docker Engine and can run as Container |Integrated inside Docker engine
Needs external KV store like Consul, etcd|No need of separate external KV store
Service model not available|Service model is available. This provides features like scaling, rolling update, service discovery, load balancing and routing mesh
Communication not secure|Both control and data plane is secure
Integrated with machine and compose|Not yet integrated with machine and compose as of release 1.12. Will be integrated in the upcoming releases

下边是SwarmKit与SwarmNext的对比：  

SwarmKit|SwarmNext
--------------|---------------------
Plumbing opensource project|Swarmkit used within SwarmNext and tightly integrated with Docker Engine
Swarmkit needs to built and run separately|Docker 1.12 comes integrated with SwarmNext
No service discovery, load balancing and routing mesh|Service discovery, load balancing and routing mesh available
Use swarmctl CLI|Use regular Docker CLI

### Sample Application   
下边是一个非常简单的应用。该应用时一个高可用的web投票服务，可以通过client访问。       
client的请求会被负载均衡到各个可用的web服务上。     
应用使用overlay网络，我们将使用Swarm、SwarmNext、SwarmKit进行部署。

![vote_web_system](https://sreeninet.files.wordpress.com/2016/07/swarm1.png?w=301&h=162)

#### 前提
本文中使用docker-machine0.8.0-rc1 ，docker1.12.0-rc3.
“smakam/myubuntu” 容器使用的是ubuntu系统，加下一些比如curl的工具来展示负载均衡。   



