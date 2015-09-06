..  
声明：   
本博客欢迎转发，但请保留原作者信息!   
博客地址：http://blog.csdn.net/halcyonbaby   
新浪微博：[@寻觅神迹]( www.weibo.com/u/2230330930)

内容系本人学习、研究和总结，如有雷同，实属荣幸！   

-----
### 启动一个完全基于容器隔离的rkt实例


### 启动一个基于VM隔离的rkt实例
<pre><code>[root@localhost rkt-v0.8.0]# rkt run --stage1-image=stage1-lkvm.aci --private-net  coreos.com/etcd:v2.0.9
rkt: searching for app image coreos.com/etcd:v2.0.9
discovery failed for "coreos.com/etcd:v2.0.9": Get http://coreos.com?ac-discovery=1: dial tcp: i/o timeout. Trying to find image in the store.
2015/09/06 03:12:45 Preparing stage1
2015/09/06 03:12:46 Loading image sha512-91e98d7f1679a097c878203c9659f2a26ae394656b3147963324c61fa3832f15
2015/09/06 03:12:46 Writing pod manifest
2015/09/06 03:12:46 Setting up stage1
2015/09/06 03:12:46 Writing image manifest
2015/09/06 03:12:46 Wrote filesystem to /var/lib/rkt/pods/run/8d4ce168-6825-4fbb-b52b-738a3c891a9d
2015/09/06 03:12:46 Writing image manifest
2015/09/06 03:12:46 Pivoting to filesystem /var/lib/rkt/pods/run/8d4ce168-6825-4fbb-b52b-738a3c891a9d
2015/09/06 03:12:46 Execing /init
...
[root@localhost temp]# ps -ef|grep lkvm
root      2006  1928  2 03:12 pts/2    00:00:06 ./stage1/rootfs/lkvm run --name rkt-8d4ce168-6825-4fbb-b52b-738a3c891a9d --no-dhcp --cpu 1 --mem 128 --console=virtio --kernel stage1/rootfs/bzImage --disk stage1/rootfs --params console=hvc0 init=/usr/lib/systemd/systemd no_timer_check noreplace-smp systemd.default_standard_error=journal+console systemd.default_standard_output=journal+console ip=172.16.28.5::172.16.28.4:255.255.255.254::eth0::: tsc=reliable MACHINEID=8d4ce168-6825-4fbb-b52b-738a3c891a9d quiet --network mode=tap,tapif=tap0,host_ip=172.16.28.4,guest_ip=172.16.28.5
</code></pre>

### 遇到的问题 
1. permission denied   
现象如下：  
<pre><code>[root@localhost rkt-v0.8.0]# rkt run coreos.com/etcd:v2.0.9
rkt: searching for app image coreos.com/etcd:v2.0.9
discovery failed for "coreos.com/etcd:v2.0.9": Get http://coreos.com?ac-discovery=1: dial tcp: i/o timeout. Trying to find image in the store.
2015/09/01 22:08:14 Preparing stage1
2015/09/01 22:08:15 Loading image sha512-91e98d7f1679a097c878203c9659f2a26ae394656b3147963324c61fa3832f15
2015/09/01 22:08:15 Writing pod manifest
2015/09/01 22:08:15 Setting up stage1
2015/09/01 22:08:15 Writing image manifest
2015/09/01 22:08:15 Wrote filesystem to /var/lib/rkt/pods/run/46bfa529-32c5-4584-9a8f-c1e744c6251f
2015/09/01 22:08:15 Writing image manifest
2015/09/01 22:08:15 Pivoting to filesystem /var/lib/rkt/pods/run/46bfa529-32c5-4584-9a8f-c1e744c6251f
2015/09/01 22:08:15 Execing /init
Failed to load pod: failed reading pod manifest: open pod: permission denied
</code></pre>
问题原因：  
rkt与selinux冲突。比较简单的做法是使用setenforce 0关闭selinux。   

### 参考
1. https://github.com/coreos/rkt
2. https://coreos.com/blog/rkt-0.8-with-new-vm-support/


