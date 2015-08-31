..  
声明：   
本博客欢迎转发，但请保留原作者信息!   
博客地址：http://blog.csdn.net/halcyonbaby   
新浪微博：[@寻觅神迹]( www.weibo.com/u/2230330930)

内容系本人学习、研究和总结，如有雷同，实属荣幸！   

-----
### Clear Linux/Clear container
Clear Linux/Clear container是由intel在今年5月份推出的新技术。   
Clear Linux是Intel提供的面向云场景的linux发行版。  
Clear Container是Clear Linux中的一项技术，旨在提供安全容器。
目标是让用户可以充分使用虚拟机的隔离，同时拥有容器的部署能力。  
![image](http://img.deusm.com/informationweek/2015/05/1320536/helicopter-598748_640.jpg)
### Clear Linux介绍  
Clear Linux是Intel提供的主要面向云的linux 发行版。  
Clear Linux的目的不是通用Linux发行版，主要是展示Intel Architecture的技术。    
Clear Linux不支持GUI和printing。

#### 特性  
- 支持AutoFDO技术  
编译程序时进行自动优化。
- 支持Clear Container技术
提供安全容器技术。  
- Stateless
- Software update   
    - OS整体更新
    - 更新支持差分
    - 两种更新模式（即时生效、或者下次启动生效（基于btrfts创建快照，更新到快照中）)
- All debug information, all the time

---
### Clear Container介绍
Intel通过将虚拟机和容器结合起来，提供一种安全容器（Clear Container）。   
这种容器相对于普通虚拟机开销更小，启动更快；相对于普通容器更加安全。
启动一个安全容器，它使用虚拟化技术，需要**150毫秒**，每个容器内存额外消耗大概是**18到20MB**。
### 原理  
主要在以下几点做了优化工作。  
#### hypervisor优化  
使用kvmtool（启动时间30ms，不需要启动UEFI/BIOS等）而非qemu-kvm（启动时间300-500ms），同时对kvmtool进行了优化。    
使kvmtool在内核中执行，而且不需要做内核的解压缩。  

#### 内核  
针对虚拟硬件，改进了内核启动时的硬件初始化。 

#### 用户空间
使用SystemD加快用户空间的创建速度。 
#### 内存消耗
基于DAX技术和KSM技术减少内存消耗。

### 实践


---
### 参考
1. 原理介绍  
（中文）http://dockone.io/article/388    
（英文）https://lwn.net/Articles/644675/    
2. 官方介绍  
https://clearlinux.org  


