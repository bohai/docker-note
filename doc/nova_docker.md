### nova-docker现状
nova-docker插件h版出现，但是在i版本从nova中移出，作为孵化项目培养。   
当时给出的解释是，希望能更快的进行迭代开发，支持cinder和neutron。并计划在K版本release时重新进入。  

### nova-docker的架构  
目前的架构如下（其中docker registry已经不需要了）。   

<img src="https://wiki.openstack.org/w/images/6/6c/Docker-under-the-hood.png" alt="nova_docker" title="nova_docker" width="400" />   

从图中可以看出，这种使用方法，docker相当于一种新的hypervisor。  
把容器当做虚拟机来使用。  

其中容器镜像通过docker save保存成tar包，放置在glance上管理。   
创建容器时，从glance上下载容器镜像，利用（docker load）加载并启动容器镜像。  

### 存储能力     

### 网络能力   


参考：  
1. http://www.opencontrail.org/openstack-docker-opencontrail/
2. http://technodrone.blogspot.com/2014/10/nova-docker-on-juno.html  
