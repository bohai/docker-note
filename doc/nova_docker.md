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

### 支持功能   
支持容器创建/删除/软删除/重启/暂停/解除暂定/停止/开始。  
支持对容器创建快照，支持基于快照恢复容器。  
支持对容器设置安全组规则/插拔网卡。  
查询docker节点上CPU/内存使用情况/查询可用节点。  
查询docker容器。  
查询容器console输出。  
支持neutron网络/nova-network网络。  
支持绑定浮动IP。  

不支持共享存储。  
不支持挂卷/卸卷操作。  
不支持迁移，rescue等操作。  

容器使用的是本地存储，不能使用cinder共享存储。

### 网络实现       
查看容器的namespace:  
<pre><code>
[root@localhost ~]# docker ps --no-trunc
CONTAINER ID                                                       IMAGE                    COMMAND             CREATED             STATUS              PORTS               NAMES
54ba6c67de05b8c5ddb824497eae0071f902dcdea05ce93109d9791453dfeb17   tutum/wordpress:latest   "/run.sh"           15 hours ago        Up 15 hours                             nova-ee2edd99-a64c-4701-84ad-faccd3b1a246
[root@localhost ~]# ip netns list
54ba6c67de05b8c5ddb824497eae0071f902dcdea05ce93109d9791453dfeb17
qdhcp-78277811-dc20-47c0-8319-58894843e3d4
3ce4e73bcfeb64b994a5bf87c7f49553ca3583308b93878a07679a742661b0a4
qdhcp-bc557a68-425e-4f24-bb6c-627500647856
ee3b2cc56a0ccae387371cf8eb6ad7f43712cf1cbdc66bf46af77f3c929be34a
qrouter-818c4149-355d-4409-8dda-f412da898ff0
</code></pre>
查看namespace中网络：  
<pre><code>
[root@localhost ~]# ip netns exec 54ba6c67de05b8c5ddb824497eae0071f902dcdea05ce93109d9791453dfeb17 ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
28: nse54c9783-26: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether fa:16:3e:d8:9b:e8 brd ff:ff:ff:ff:ff:ff
    inet 10.0.0.2/24 brd 10.0.0.255 scope global nse54c9783-26
       valid_lft forever preferred_lft forever
    inet6 fe80::f816:3eff:fed8:9be8/64 scope link
       valid_lft forever preferred_lft forever
</code></pre>

参考：  
1. http://www.opencontrail.org/openstack-docker-opencontrail/   
2. http://technodrone.blogspot.com/2014/10/nova-docker-on-juno.html    
