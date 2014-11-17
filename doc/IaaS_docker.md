### IaaS进入Container Service2.0 
近来Google、Amazon接连发布基于容器（其实主要是Docker)的新业务。
+ 2014.11.05  Google发布Google Container engine  
+ 2014.11.13  Amazon发布AWS Container Service  

相比于之前简单与虚拟机集成的方式，这些新服务对Docker的支持进一步加强。  
用户真正可以方便的对容器的方式进行业务管理，虚拟机仅仅作为容器集群资源的提供者。
接下来，我们可以等待Azure的新容器服务发布了。

如果我们把之前IaaS公有云提供商的产品看做conrtainer service1.0, 这轮新发布的产品
相当于2.0升级版。  

在1.0中，各厂商引入API、CLI方式向用户提供在虚拟机中创建容器的简单能力。  
在2.0中，各厂商引入容器集群、业务（一组容器，Task/Pods）的概念。对基于容器开发的用户来说，似乎在淡化虚拟机存在。
用户完全以容器的方式进行管理和业务发放。在资源不足时，才需要往容器集群中增加新的节点（虚拟机）。  

目前国内厂商刚刚开始1.0的支持。

### Amazon与Google容器方案对比  
##### 对象对比  
###### 集群管理    
Google的Cluster有一组虚拟机组成，其中包含了一个master节点和多个node节点。Google选择了自己主导的kubernetes作为集群管理工具。Google提供了Replication Controller确保业务的多个实例的同时运行。用于提高业务的可靠性。     
Amazon的Cluster也是由一组虚拟机（在一个region，可以在多个AZ中）组成。每个集群可以创建一个scheduler，负责容器在集群中的管理。
###### 业务管理    
Google提供了Pods，用来管理一个包含多个容器的业务。
Amazon提供给了Task Define定义一个包含多个容器的业务，Task是Task Define的实例。  
###### 镜像   
Amazon提供了ECS-Enabled AMI（其中包含了agent软件）供用户使用。后续第三方支持Google container service的AMI镜像也将提供。  
Google没有类似的暴露，而是直接帮助用户建立一个kubernetes CLuster。  
###### 特别的 
Google还提供给了Service的概念。因为Pods都是临时的，随时可能失效。Service用来完成对Pods的路由，避免Pods消失带来的业务不可访问。  
###### 使用过程
+ Amazon  
1. 创建Cluster  
2. 创建Task define，并注册到Cluster中  
3. 创建虚拟机，并注册到CLuster中  
4. 根据Task define创建若干个Task实例  
5. 提供服务。然后监控cluster情况，进行Cluseter中虚拟机的增减  
+ Google   
1. 创建Cluster
2. 创建Pods
3. 配置外网通信的firewall

