..  
声明：   
本博客欢迎转发，但请保留原作者信息!   
博客地址：http://blog.csdn.net/halcyonbaby   
新浪微博：[@寻觅神迹]( www.weibo.com/u/2230330930)

内容系本人学习、研究和总结，如有雷同，实属荣幸！   

-----
# Docker1.9后的network
### 介绍与使用
1.9之后，在Docker中network从实验特性转为正式特性发布。   
从命令行可以看到新增如下命令：
<pre><code>[root@localhost system]# docker help network

Usage:  docker network [OPTIONS] COMMAND [OPTIONS]

Commands:
  create                   Create a network
  connect                  Connect container to a network
  disconnect               Disconnect container from a network
  inspect                  Display detailed network information
  ls                       List all networks
  rm                       Remove a network

Run 'docker network COMMAND --help' for more information on a command.

  --help=false       Print usage
</code></pre>
可以看到Docker daemon启动后默认创建了3个网络：
分别使用了bridge、null、host三种内置network driver。
<pre><code>[root@localhost system]# docker network ls
NETWORK ID          NAME                DRIVER
f280d6a13422        bridge              bridge
f5d11bed22a2        none                null
18642f53648f        host                host
</code></pre>
我们来仔细看下三个网络的详细信息：  
Name是network的名字，用户可以随意定义。  
Id是network内部的uuid，全局唯一。   
Scope目前有两个值“local”、“remote”，表示是本机网络还是多机网络。  
Driver是指network driver的名字。  
IPAM是负责IP管理发放的driver名字与配置信息（我们在bridge网络中可以看到该信息）。  
Container内记录了使用这个网络的容器的信息。  
Options内记录了driver所需的各种配置信息。  
<pre><code>[root@localhost temp]# docker network inspect none
[
    {
        "Name": "none",
        "Id": "1abfa4750ada3be20927c3c168468f9a64efd10705d3be8958ae1eef784b28ef",
        "Scope": "local",
        "Driver": "null",
        "IPAM": {
            "Driver": "default",
            "Config": []
        },
        "Containers": {},
        "Options": {}
    }
]
[root@localhost temp]# docker network inspect host
[
    {
        "Name": "host",
        "Id": "001c9c9047d90efff0b64bf80e49ff7ec33421374b2c895169a0f9e096eb791d",
        "Scope": "local",
        "Driver": "host",
        "IPAM": {
            "Driver": "default",
            "Config": []
        },
        "Containers": {},
        "Options": {}
    }
]
[root@localhost temp]# docker network inspect bridge
[
    {
        "Name": "bridge",
        "Id": "201fbcb64b75977889f5d9c1e88c756308a090eb611397dbd0bb5c824d429276",
        "Scope": "local",
        "Driver": "bridge",
        "IPAM": {
            "Driver": "default",
            "Config": [
                {
                    "Subnet": "172.17.42.1/16",
                    "Gateway": "172.17.42.1"
                }
            ]
        },
        "Containers": {
            "4d4d37853115562080613393c6f605a9ec2b06c3660dfa0ca4e27f2da266773d": {
                "EndpointID": "09e332644c539cec8a9852a11d402893bc76a5559356817192657b5840fe2de3",
                "MacAddress": "02:42:ac:11:00:01",
                "IPv4Address": "172.17.0.1/16",
                "IPv6Address": ""
            }
        },

        "Options": {
            "com.docker.network.bridge.default_bridge": "true",
            "com.docker.network.bridge.enable_icc": "true",
            "com.docker.network.bridge.enable_ip_masquerade": "true",
            "com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
            "com.docker.network.bridge.name": "docker0",
            "com.docker.network.driver.mtu": "1500"
        }
    }
]
</code></pre>
容器网络的各种操作：  
-> 创建/添加/解除/删除网络
<pre><code>[root@localhost temp]# docker network create -d bridge --ip-range=192.168.1.0/24 --gateway=192.168.1.1 --subnet=192.168.1.0/24  bridge2
b18f4fb74ebd32b9f67631fd3fd842d09b97c30440efebe254a786d26811cf66
[root@localhost temp]# docker network ls
NETWORK ID          NAME                DRIVER
1abfa4750ada        none                null
001c9c9047d9        host                host
b18f4fb74ebd        bridge2             bridge
201fbcb64b75        bridge              bridge
[root@localhost temp]# docker exec vim ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
69: eth0@if70: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue state UP
    link/ether 02:42:ac:11:00:01 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:acff:fe11:1/64 scope link
       valid_lft forever preferred_lft forever
[root@localhost temp]# docker network connect bridge2 vim
[root@localhost temp]# docker exec vim ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
69: eth0@if70: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue state UP
    link/ether 02:42:ac:11:00:01 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:acff:fe11:1/64 scope link
       valid_lft forever preferred_lft forever
72: eth1@if73: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue state UP
    link/ether 02:42:c0:a8:01:02 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.2/24 scope global eth1
       valid_lft forever preferred_lft forever
    inet6 fe80::42:c0ff:fea8:102/64 scope link
       valid_lft forever preferred_lft forever
[root@localhost temp]# docker network disconnect bridge2 vim
[root@localhost temp]# docker exec vim ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
69: eth0@if70: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue state UP
    link/ether 02:42:ac:11:00:01 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:acff:fe11:1/64 scope link
       valid_lft forever preferred_lft forever
[root@localhost temp]# docker network rm bridge2
[root@localhost temp]# docker network ls
NETWORK ID          NAME                DRIVER
1abfa4750ada        none                null
001c9c9047d9        host                host
201fbcb64b75        bridge              bridge
</code></pre>
### driver plugin机制与driver plugin实现  
Docker插件一览：  
http://docs.docker.com/engine/extend/plugins/


### libnetwork与docker


