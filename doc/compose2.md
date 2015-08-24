..  
声明：   
本博客欢迎转发，但请保留原作者信息!   
博客地址：http://blog.csdn.net/halcyonbaby   
新浪微博：[@寻觅神迹]( www.weibo.com/u/2230330930)

内容系本人学习、研究和总结，如有雷同，实属荣幸！   

-----
>以下内容基于Compose1.4。

# Docker/ompose分析
### Compose是什么？
Compose是Docker公司提供的开源的编排部署工具。Compose的前身是Fig，使用Python代码编写。
License为Apache2.0，对商业友好。
### 为什么需要Compose？
因为用户的实际应用是复杂的，可能由多个容器组成，容器间存在关系，使用上可能需要重复多次部署。  
因此，需要一定的编排部署能力来简化这个操作。
### Compose的架构
Compose目前只提供命令行工具，没有Daemon存在。Compose与Docker紧密结合，目前只支持Docker。
当然Compose也可以支持Swarm。  
Compose运行需要有对应的yml文件以及Dockerfile。   
通过调用Docker/Swarm的API进行容器应用的编排。     
### Compose的现状
Compose目前版本为1.4。官方推荐在开发、测试、持续集成等非生成环境使用。并不适合生产环境使用。 
### 模型
service：实际上是一个包含某种功能的容器。 
Compose的所有操作对象均为service。  
### 功能
-  build(构建yml中某个服务的镜像)
如上，web这个服务是依赖于镜像build的。在本地 也存在Dockerfile文件。
可以使用docker-compose build来构建服务的镜像。  
-  ps(查看已经启动的服务状态）
- kill(停止某个服务）
- logs(可以查看某个服务的log）
- port(打印绑定的public port）  
- pull(pull服务镜像)  
- up(启动yml定义的所有服务）
- stop(停止yml中定义的所有服务）
- start(启动被停止的yml中的所有服务）  
- kill(强行停止yml中定义的所有服务）
- rm（删除yml中定义的所有服务）
- restart(重启yml中定义的所有服务）  
- scale(扩展某个服务的个数，可以向上或向下）
- migrate-to-labels(这个没有实际尝试。根据介绍是将服务从1.2迁移到1.3带labels的版本。docker之前不支持label）
- version（查看compose的版本）

### 缺点
#### 没有Daemon
没有Deaemon，也就没有高可用、HA之说。  
但是同时没有Deamon，所用动作需要用户自己触发。AutoScaling、self healing等也就没有办法提供。
#### 模型不完整
模型相对简单，只有service。
缺乏诸如网络、存储之类的资源抽象和管理。  
也缺乏诸如kubernetes中Pod、RC、service proxy之类的抽象，由于servie本身粒度太细，操作管理起来相对麻烦。  
#### 使用Python代码编写
由于Docker社区大部分项目是Go编写的，Compose使用python不利于项目间代码共享。
所幸的是，Compose社区目前已经开始着手此事。
#### 与Docker紧密结合 
是优点也是缺点。一方面可以很好的支持Docker的最新特性，另一方面与Docker绑死。
### 未来发展
目前社区已经开始着手使用Go语言重新Compose，并以lib方式提供。  
Docker的理念是便于上层集成，也许未来会在kitematic中集成Compose的功能。 
其他第三方也可以通过各种方式进行集成。  
### 演示理解

### 代码分析
### 参考资料
1. Compose文档  
http://docs.docker.com/compose/
2. Github地址   
https://github.com/docker/compose


