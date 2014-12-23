#### 容器互联
##### link方式   
通过link方式创建容器，然后我们可以使用被link容器的别名进行访问。    
从而解除应用对IP的依赖。  
不幸的是,link方式只能解决单机容器间的互联。多机情况下，容器的互联需要其他的方式。
<pre><code>
[root@localhost ~]# docker run -i -t   mysql:latest /bin/bash
root@7afad07a05b0:/usr/local/mysql# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
79: eth0: <BROADCAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether 02:42:ac:11:00:04 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.4/16 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:acff:fe11:4/64 scope link
       valid_lft forever preferred_lft forever
       
[root@localhost ~]# docker run -i -t --link=sad_bardeen:sql  mysql:latest /bin/bash
root@931c7ab8135e:/usr/local/mysql# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
81: eth0: <BROADCAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether 02:42:ac:11:00:05 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.5/16 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:acff:fe11:5/64 scope link
       valid_lft forever preferred_lft forever
root@931c7ab8135e:/usr/local/mysql# ping sql
PING sql (172.17.0.4): 48 data bytes
56 bytes from 172.17.0.4: icmp_seq=0 ttl=64 time=0.114 ms
###可以看出来，加了一个静态dns
root@931c7ab8135e:/usr/local/mysql# cat /etc/hosts
172.17.0.5      931c7ab8135e
127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
172.17.0.4      sql
</code></pre>
##### 通过容器方式互联   
如上面所说，link只适用于一台主机。  
两台主机，docker官方推荐了如下方式连接两个容器。  
以下以wordpress+mysql的服务为例。部署在两台机器上的wordpress和mysql通过一对ambassador进行连接。  
wordpress(in vm1)--link-->ambassador1(in vm1)----socat--->ambassador2(in vm2)--link--->mysql(in vm2)   
<pre><code>
启动mysql：
sudo docker run -d --name mysql mysql
启动ambassador1：
sudo docker run -d --link mysql:mysql --name ambassador1 -p 3306:3306 ambassador  
启动ambassador2：
sudo docker run -d --name ambassador2 --expose 3306 -e MYSQL_PORT_3306_TCP=tcp://x.x.x.x:3306 ambassador  
启动wordpress:
sudo docker run -i -t --rm --link ambassador2:mysql wordpress
</code></pre>


参考：   
http://blog.csdn.net/sunset108/article/details/40856957
