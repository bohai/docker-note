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
<pre><code>[root@localhost ~]# docker ps --no-trunc
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
<pre><code>[root@localhost ~]# ip netns exec 54ba6c67de05b8c5ddb824497eae0071f902dcdea05ce93109d9791453dfeb17 ip addr
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
查看设备28的关联veth pair：
<pre><code>[root@localhost ~]# ip netns exec 54ba6c67de05b8c5ddb824497eae0071f902dcdea05ce93109d9791453dfeb17  ethtool -S nse54c9783-26
NIC statistics:
     peer_ifindex: 29
[root@localhost ~]# ip addr
...
29: tape54c9783-26: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master ovs-system state UP qlen 1000
    link/ether 82:31:7f:dc:e3:8f brd ff:ff:ff:ff:ff:ff
    inet6 fe80::8031:7fff:fedc:e38f/64 scope link
       valid_lft forever preferred_lft forever
...
</code></pre>
查看设备29关联设备：(设备挂在OVS网桥的br-int上）
<pre><code>[root@localhost ~]# ovs-vsctl show
2368aead-599b-4cd8-b2a1-dd01041e5635
    Bridge br-ex
        Port br-ex
            Interface br-ex
                type: internal
        Port "qg-83cd012e-53"
            Interface "qg-83cd012e-53"
                type: internal
    Bridge br-int
        fail_mode: secure
        Port "tapbf138559-94"
            tag: 3
            Interface "tapbf138559-94"
        Port "tape54c9783-26"
            tag: 1
            Interface "tape54c9783-26"
        Port "tap7687fcec-f0"
            tag: 2
            Interface "tap7687fcec-f0"
        Port br-int
            Interface br-int
                type: internal
        Port "qr-9712c2ca-1f"
            tag: 1
            Interface "qr-9712c2ca-1f"
                type: internal
        Port patch-tun
            Interface patch-tun
                type: patch
                options: {peer=patch-int}
        Port "tap5f8409aa-f9"
            tag: 3
            Interface "tap5f8409aa-f9"
                type: internal
        Port "tapeb9206a8-85"
            tag: 1
            Interface "tapeb9206a8-85"
                type: internal
    Bridge br-tun
        Port patch-int
            Interface patch-int
                type: patch
                options: {peer=patch-tun}
        Port br-tun
            Interface br-tun
                type: internal
    ovs_version: "2.0.0"
</code></pre>
备注：因为是个单机环境，没有给br-int配置具体的物理网卡。  
容器DHCP服务与绑定Floating IP:   
<Pre><code> //10.0.0.0/24网段的DHCP服务
[root@localhost ~]# ip netns exec qdhcp-78277811-dc20-47c0-8319-58894843e3d4 ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
27: tapeb9206a8-85: <BROADCAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN
    link/ether fa:16:3e:6e:1b:13 brd ff:ff:ff:ff:ff:ff
    inet 10.0.0.3/24 brd 10.0.0.255 scope global tapeb9206a8-85
       valid_lft forever preferred_lft forever
    inet6 fe80::f816:3eff:fe6e:1b13/64 scope link
       valid_lft forever preferred_lft forever
//可以看出通过router将内部10.0.0.0/24的网络与外部172.24.4.0/24的两个IP打通
[root@localhost ~]# ip netns exec qrouter-818c4149-355d-4409-8dda-f412da898ff0  ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
19: qr-9712c2ca-1f: <BROADCAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN
    link/ether fa:16:3e:50:18:19 brd ff:ff:ff:ff:ff:ff
    inet 10.0.0.1/24 brd 10.0.0.255 scope global qr-9712c2ca-1f
       valid_lft forever preferred_lft forever
    inet6 fe80::f816:3eff:fe50:1819/64 scope link
       valid_lft forever preferred_lft forever
20: qg-83cd012e-53: <BROADCAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN
    link/ether fa:16:3e:0d:4e:c2 brd ff:ff:ff:ff:ff:ff
    inet 172.24.4.2/24 brd 172.24.4.255 scope global qg-83cd012e-53
       valid_lft forever preferred_lft forever
    inet 172.24.4.6/32 brd 172.24.4.6 scope global qg-83cd012e-53
       valid_lft forever preferred_lft forever
    inet6 fe80::f816:3eff:fe0d:4ec2/64 scope link
       valid_lft forever preferred_lft forever
</ocde></pre>

参考：  
1. http://www.opencontrail.org/openstack-docker-opencontrail/   
2. http://technodrone.blogspot.com/2014/10/nova-docker-on-juno.html    
