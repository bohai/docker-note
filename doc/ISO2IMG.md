..  
声明：   
本博客欢迎转发，但请保留原作者信息!   
博客地址：http://blog.csdn.net/halcyonbaby   
新浪微博：[@寻觅神迹]( www.weibo.com/u/2230330930)

内容系本人学习、研究和总结，如有雷同，实属荣幸！   

-----
openstack镜像制作
=======

要在openstack上创建虚拟机，必然要使用到虚拟机镜像。   
对于普通用户，可以使用已经创建好的虚拟机镜像。一般是操作系统官方构建并提供的。

某些用户可以有自己独特的需求，需要定制特别的虚拟机镜像。
这时候主要涉及镜像更改/镜像格式转化/镜像创建。 
用户可以参照[openstack官方文档](http://docs.openstack.org/zh_CN/image-guide/content/ch_preface.html)。

### 镜像更改
镜像格式更改，有多种工具和方法。
* guestfs提供的guestfish和guestmount。  
  guestfish比较有意思，guestfish会启动一个虚拟机，然后通过串口与虚拟机内进行通信。我们可以基于此，对虚拟机内进行修改。
* virt-*工具。  
* loop回环设备的方式，修改镜像内容。   

### 镜像格式转换
一般是使用qemu-img进行转换。  
virtualBox有一个转换为Raw的工具。 

### 镜像创建
一般有两种方式。
手工构建，方法上来说比较简单，但是过程比较繁琐。适合开发者，或者小规模情况下使用。   
自动构建，openstack官方文档也提供了一些构建工具和方法。   

自动构建工具目前有很多，主要有diskimage-builder，Oz，VMBuilder，VeeWee，Packer，ImageFactory，SUSE Studio。  
其中，diskimage-builder是openstack中TripleO的子项目，在各个工具中功能相对完善，支持主要的Linux操作系统（fedora/centos/redhat/ubuntu/debian）
)的镜像制作。  

diskimage-builder的安装比较简单，直接clone代码，设置环境变量即可运行。  
<pre><code># disk-image-create ubuntu vm</code></pre>

diskimage-builder支持定制element，即镜像中包含的元素。（比如创建用户，安装软件包，进行某种配置）  
用户可以根据需要进行定义，然后再使用disk-image-create时指定。具体参考[diskimage-builder指导](http://docs.openstack.org/developer/diskimage-builder/)。

diskimage-builder的原理也比较简单，是在主机上创建虚拟机镜像，然后通过挂载/chroot方式，通过kickstart自动完成镜像内容的安装。  
elements比较像程序中的接口/插件机制，将element中规定目录下的定制脚本执行，完成对镜像的定制。   
整个过程并不需要启动虚拟机。 

上边工具主要是Linux镜像的制作，并不支持windows镜像的自动制作。  

我也搜索了下，windows镜像自动制作也是可能的，但是并不清楚，目前为什么没有集成进去。可能是创建过程差异略大。Windows镜像的创建，
一般需要创建虚拟机，通过应答文件完成OS的自动安装。应答文件一般放在软盘中，需要创建一个虚拟软盘文件。   



