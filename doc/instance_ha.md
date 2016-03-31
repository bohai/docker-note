..  
声明：   
本博客欢迎转发，但请保留原作者信息!   
博客地址：http://blog.csdn.net/halcyonbaby   
新浪微博：[@寻觅神迹]( www.weibo.com/u/2230330930)

内容系本人学习、研究和总结，如有雷同，实属荣幸！   

-----
# 公有云上虚拟机故障恢复
## AWS  
## 阿里云  
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
参考： 
https://cloud.google.com/compute/docs/reference/latest/instances/setScheduling   
https://cloud.google.com/compute/docs/instances/setting-instance-scheduling-options   
https://cloud.google.com/compute/docs/tutorials/robustsystems
