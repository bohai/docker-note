..  
声明：   
本博客欢迎转发，但请保留原作者信息!   
博客地址：http://blog.csdn.net/halcyonbaby   
新浪微博：@寻觅神迹

内容系本人学习、研究和总结，如有雷同，实属荣幸！   

----------

Flocker是什么
=====
Flocker提供了开源容器数据卷管理系统。   
Flocker提供了数据迁移的工具，从而解决了有状态服务的容器化难题。尤其适用于数据库这样的容器。  

通常，容器的数据卷与单个server绑定，Flocker数据卷，则可以随容器迁移而迁移。Flocker为实现有状态的 微服务提供了便利。   
![compare](https://docs.clusterhq.com/en/1.0.3/_images/flocker-v-native-containers.svg)

Flocker的整体架构
=====
![flocker architecture](https://docs.clusterhq.com/en/1.0.3/_images/flocker-architecture.svg)

Flocker主要分两部分control和agent，control对外提供API，并于agent通信，完成以下功能：

 - 部署跨节点的多容器应用
 - 节点间带卷迁移容器
 - 在容器改变host时，随之挂卷／卸卷
 - 在服务器间迁移本地数据卷  

Flocker的原理
=====
Flocker control会管理卷的所在位置，并根据需要进行修改。  
Flocker agent根据control的设置，修改本地状态。进行卷的挂载／卸载。  
更具体的原理下次再说。。。
