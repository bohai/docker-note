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

Docker swarm mode和swarm存在本质区别，但是却使用了swarm这个易于混淆的名字。  
我觉得docker社区应该考虑换个名字。另外一点同样增加了这个混淆，native swarm会在1.12继续支持，从而提供兼容性。   

这篇Blog中，我们使用“Swarm”表示老的swarm项目，“Swarmkit”表示新开源的swarmkit项目，“SwarmNext”表示docker swarm mode。   





