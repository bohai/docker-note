..  
声明：   
本博客欢迎转发，但请保留原作者信息!   
博客地址：http://blog.csdn.net/halcyonbaby   
新浪微博：寻觅神迹

内容系本人学习、研究和总结，如有雷同，实属荣幸！   

====================================
Amazon EC2 Container Service笔记
====================================
Amazon EC2 Container Service（ECS）是一个高度可扩展、高可用、低延迟的容器管理服务。  
ECS支持Docker，用户可以轻松在Amazon EC2实例集群上运行应用。  

ECS的包含的基本组件：    
![ECS] (http://cdn2.infoqstatic.com/statics_s1_20150722-0039/resource/news/2015/07/Amazon-ECS/zh/resources/1.png)

组件情况：  
集群管理器，负责处理集群协调和状态管理任务。
ECS agent，允许Amazon ECS与EC2实例通信，并在用户/调度器请求时启动、停止、监控容器。(开源、apache协议）
Key/value store：提供集群信息的存储。
API：提供用户API，可以实现自己的的scheduler。甚至可以与Mesos进行集成。目前已经实现了
ECSSchedulerDriver。

模型情况：  
Cluster:一组container instance，task运行在Cluster上。   
Container instance：运行Amazon ECS agent的EC2 instance，可以注册到某个cluster。  
Task Define:描述一个应用，可能含有一个或多个容器的定义。    
Scheduler： 负责task运行位置的管理。  
Service： 同时运行和管理一个或多个task definition。（有点像kubernetes中RC的概念+loadbalanace）    
Task： 运行在一个container instance上的task definition实例（类似于kubernetes的Pod）。  
Container： Linux container，是task的一部分。 




