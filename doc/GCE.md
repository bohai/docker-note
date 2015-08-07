..  
声明：   
本博客欢迎转发，但请保留原作者信息!   
博客地址：http://blog.csdn.net/halcyonbaby   
新浪微博：[@寻觅神迹]( www.weibo.com/u/2230330930)

内容系本人学习、研究和总结，如有雷同，实属荣幸！   

-----

# Google Container Engine
## 简介  
Google Container Engine是google去年推出的容器集群管理服务。对应与Amazon家的ECS服务。  
目前处于Beta测试阶段，相信不久后就会GA。  
目前阶段，Google Container Engine服务没有额外费用（虚拟机本身还是要收费的，但是提供了部分免费试用额度）。
GA后根据集群大小进行收费：   
Standard cluster规模费用为$0.15/H。  
Bisic Cluster规模（5个虚拟机节点以下）免费。可以升级到standard cluster。  
## 概念
Google Container Engine本身基于Google的开源项目Kubernetes。所以其中的概念与Kubernetes完全一致。  

- Container Clusters  
Container cluster由一组运行Kubernetes的虚拟机实例组成。它包含了若干node实例，和Kubernetes master endpoint。  
Cluster是Pods、Replication Controllers、Services的基础。  
- Pods  
> A pod models an application-specific "logical host" in a containerized environment.     

由一个或多个container组成，运行在相同的服务器或者虚拟机中。是调度的最小单位。  
Pods内的容器共享数据（能看到相同的卷、目录）、通信（网络namespace相同，可以使用localhost通信）。

- Replication Controllers  
监控、管理Pod副本的个数。  
主要用途：Rescheduling、Scaling、Rolling updates、Multiple release tracks。  
- Services  
提供对Pods服务的路由。
## 基本功能  
- 创建Clusters
- Resize Clusters
- 创建Pods
- 创建Replication Controller
- 创建服务  
- Resize Replication Controller
- 滚动更新
- 更新Cluster
## 过去半年的重要更新  
- 支持Kubernetes1.0
- Google container service的master node不再通过创建instance创建。而是以托管服务形式提供（由Google提供可靠性保证）。   
...
