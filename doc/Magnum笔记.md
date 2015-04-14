..  
声明：   
本博客欢迎转发，但请保留原作者信息!   
博客地址：http://blog.csdn.net/halcyonbaby   
新浪微博：寻觅神迹

内容系本人学习、研究和总结，如有雷同，实属荣幸！   

==================
Magnum笔记
==================
+ 现状  
openstack通过nova driver的方式支持容器。但是虚拟机和容器，本质上存在差异。    
因此nova docker不能完整的支持容器的能力。  

+ 为什么有magnum  
让openstack顺应趋势，不仅在管理虚拟机和裸机上有竞争力。在容器的管理也更有竞争力。  
但是nova是以instance为中心的，模型并不适合容器。 
Magnum提供了全新的API服务，用来像nova一样管理容器。  

+ Magnum的目标场景  
    + 异构各种容器技术  比如LXC、OpenVZ、Docker  
    + 应用迁移          使用容器技术将应用在各种环境中部署迁移
    + 应用合并          将部署在多台机器上的应用合并更少的服务器上。提供硬件利用率。
    + 容器中心          用户只用关心容器的创建删除。容器所需的资源（比如虚拟机）自动分配。
    + 平台集成          集成kubernetes、mesos等平台的能力。
    + 容器网络          为容器提供overlay的网络。
    + 安全的原生API     提供两种操作模式。①通过Magnum管理Pods、RC、Service。②通过kubernetes或者docker原生API，管理Pods、RC、Service。
    + 支持多云、多Region能力

+ 支持三种容器运行模式
    + 裸机中
    + 虚拟机中
    + 容器中嵌套   



