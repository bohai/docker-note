..  
声明：   
本博客欢迎转发，但请保留原作者信息!   
博客地址：http://blog.csdn.net/halcyonbaby   
新浪微博：[@寻觅神迹]( www.weibo.com/u/2230330930)

内容系本人学习、研究和总结，如有雷同，实属荣幸！   

-----
# 公有云上虚拟机故障恢复
## AWS  
在亚马逊，可以创建 Amazon CloudWatch 警报用于监控 Amazon EC2 实例，并且在实例受损（由于发生底层硬件故障或需要 AWS 参与才能修复的问题）时自动恢复实例。
导致系统状态检查出现故障（StatusCheckFailed_System警报）的问题示例包括：
+ 网络连接丢失  
+ 系统电源损耗  
+ 物理主机上的软件问题  
+ 物理主机上的硬件问题  

针对该StatusCheckFailed_System故障警报，用户可以在设置自动恢复操作。   

> "对实例恢复故障进行排除故障

>以下问题可能会导致实例自动恢复失败：

>替换硬件的临时容量不足。
该实例有一个附加实例存储，而自动实例恢复不支持该配置。
一项进行中的服务运行状况仪表板事件使恢复过程无法成功执行。有关服务可用性的最新信息，请参阅 http://status.aws.amazon.com。
该实例已达到每天最多三次的恢复尝试操作限制。
自动恢复过程每天最多针对三个不同的故障尝试恢复您的实例。如果实例系统状态检查故障仍然存在，建议您手动启动和停止实例。有关更多信息，请参阅 停止和启动您的实例。

>如果自动恢复失败，并且确定硬件性能下降是初始系统状态检查失败的根本原因，那么您的实例随后可能会被停用。"

## GCE  
GCE主要对两类事件进行处理：
+ onHostMaintenance（主要是维护事件的应对）  
  +  migrate（默认）
  +  terminate
+ automaticRestart（主要是虚拟机异常crash或者Google Engine关闭）    
  +  true（默认）
  +  false   

对维护事件，默认会进行热迁移，用户也可以选择处理是关闭。  
对虚拟机异常crash、或者google engine关闭虚拟机（非用户进行的关闭），默认处理为restart。用户也可以选择为不处理。 

用户可以通过console、API、cmd对如上策略进行设置。   

参考：   
https://cloud.google.com/compute/docs/reference/latest/instances/setScheduling   
https://cloud.google.com/compute/docs/instances/setting-instance-scheduling-options   
https://cloud.google.com/compute/docs/tutorials/robustsystems

## 阿里云  
>“什么是宕机迁移，如何避免因为宕机迁移导致的服务不可用
云服务器是部署在物理机上的，底层物理机性能出现异常或者其他原因都会导致物理机宕机，当检测到云服务器所在的物理机机发生故障，系统会启动保护性迁移，将您的服务器迁移到性能正常的宿主机上 ，一旦发生宕机迁移，您的服务器就会被重启，如果您希望您的服务器重启以后应用服务器自动恢复，需要您把应用程序设置成开机自动启动，如果应用服务连接的数据库，需要在程序中设置成自动重连机制。”   

阿里云对故障的处理是，通过内部进行虚拟机HA处理。   
将故障节点上的虚拟机重新拉起。  

目前阿里云的监控，并未提供监控事件定制故障处理。   


