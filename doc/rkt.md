..  
声明：   
本博客欢迎转发，但请保留原作者信息!   
博客地址：http://blog.csdn.net/halcyonbaby   
新浪微博：[@寻觅神迹]( www.weibo.com/u/2230330930)

内容系本人学习、研究和总结，如有雷同，实属荣幸！   

-----
### 启动一个完全基于容器隔离的rkt实例
可以看出来基于nspaswn创建rkt实例。  
<pre><code>[root@localhost temp]# rkt run coreos.com/etcd:v2.0.9
rkt: searching for app image coreos.com/etcd:v2.0.9
discovery failed for "coreos.com/etcd:v2.0.9": Get http://coreos.com?ac-discovery=1: dial tcp: i/o timeout. Trying to find image in the store.
2015/09/06 03:08:53 Preparing stage1
2015/09/06 03:08:53 Loading image sha512-91e98d7f1679a097c878203c9659f2a26ae394656b3147963324c61fa3832f15
2015/09/06 03:08:53 Writing pod manifest
2015/09/06 03:08:53 Setting up stage1
2015/09/06 03:08:53 Writing image manifest
2015/09/06 03:08:53 Wrote filesystem to /var/lib/rkt/pods/run/dc2e04df-630f-4b6c-bb20-860728f33b24
2015/09/06 03:08:53 Writing image manifest
2015/09/06 03:08:53 Pivoting to filesystem /var/lib/rkt/pods/run/dc2e04df-630f-4b6c-bb20-860728f33b24
2015/09/06 03:08:53 Execing /init
[root@localhost temp]# ps -ef|grep 1914
root      1914  1909  0 03:08 ?        00:00:02 /etcd
root      2214  2184  0 03:19 pts/4    00:00:00 grep --color=auto 1914
[root@localhost temp]# ps -ef|grep 1909
root      1909  1862  0 03:08 ?        00:00:00 /usr/lib/systemd/systemd --default-standard-output=tty --log-target=null --log-level=warning --show-status=0
root      1910  1909  0 03:08 ?        00:00:00 /usr/lib/systemd/systemd-journald
root      1914  1909  0 03:08 ?        00:00:02 /etcd
root      2216  2184  0 03:19 pts/4    00:00:00 grep --color=auto 1909
[root@localhost temp]# ps -ef|grep 1862
root      1862  1822  0 03:08 pts/1    00:00:00 stage1/rootfs/usr/lib/ld-linux-x86-64.so.2 stage1/rootfs/usr/bin/systemd-nspawn --boot --register=true --link-journal=try-guest --quiet --uuid=dc2e04df-630f-4b6c-bb20-860728f33b24 --machine=rkt-dc2e04df-630f-4b6c-bb20-860728f33b24 --directory=stage1/rootfs -- --default-standard-output=tty --log-target=null --log-level=warning --show-status=0
</code></pre>

### 启动一个基于VM隔离的rkt实例
可以看到基于lkvm创建容器。
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

#### 原理分析
我们可以看出来“console=hvc0 init=/usr/lib/systemd/systemd no_timer_check noreplace-smp systemd.default_standard_error=journal+console systemd.default_standard_output=journal+console ip=172.16.28.5::172.16.28.4:255.255.255.254::eth0::: tsc=reliable MACHINEID=8d4ce168-6825-4fbb-b52b-738a3c891a9d quiet”这串是内核的启动参数。   

kernel使用的是stage1/rootfs/bzImage。
<pre><code>[root@localhost temp]# mountpoint /var/lib/rkt/pods/run/8d4ce168-6825-4fbb-b52b-738a3c891a9d/stage1/rootfs/
/var/lib/rkt/pods/run/8d4ce168-6825-4fbb-b52b-738a3c891a9d/stage1/rootfs/ is a mountpoint
[root@localhost temp]# mountpoint /var/lib/rkt/pods/run/8d4ce168-6825-4fbb-b52b-738a3c891a9d/stage1/rootfs/opt/stage2/etcd/rootfs/
/var/lib/rkt/pods/run/8d4ce168-6825-4fbb-b52b-738a3c891a9d/stage1/rootfs/opt/stage2/etcd/rootfs/ is a mountpoint
[root@localhost temp]# mount
...
overlay on /var/lib/rkt/pods/run/8d4ce168-6825-4fbb-b52b-738a3c891a9d/stage1/rootfs type overlay (rw,relatime,context="system_u:object_r:svirt_sandbox_file_t:s0:c353,c500",lowerdir=/var/lib/rkt/cas/tree/sha512-ddff10a5cf165fc34d66a70542edbcd6eda23144e6259cd2f06ad503625fccb6/rootfs,upperdir=/var/lib/rkt/pods/run/8d4ce168-6825-4fbb-b52b-738a3c891a9d/overlay/sha512-ddff10a5cf165fc34d66a70542edbcd6eda23144e6259cd2f06ad503625fccb6/upper,workdir=/var/lib/rkt/pods/run/8d4ce168-6825-4fbb-b52b-738a3c891a9d/overlay/sha512-ddff10a5cf165fc34d66a70542edbcd6eda23144e6259cd2f06ad503625fccb6/work)
overlay on /var/lib/rkt/pods/run/8d4ce168-6825-4fbb-b52b-738a3c891a9d/stage1/rootfs/opt/stage2/etcd/rootfs type overlay (rw,relatime,context="system_u:object_r:svirt_sandbox_file_t:s0:c353,c500",lowerdir=/var/lib/rkt/cas/tree/sha512-91e98d7f1679a097c878203c9659f2a26ae394656b3147963324c61fa3832f15/rootfs,upperdir=/var/lib/rkt/pods/run/8d4ce168-6825-4fbb-b52b-738a3c891a9d/overlay/sha512-91e98d7f1679a097c878203c9659f2a26ae394656b3147963324c61fa3832f15/upper/etcd,workdir=/var/lib/rkt/pods/run/8d4ce168-6825-4fbb-b52b-738a3c891a9d/overlay/sha512-91e98d7f1679a097c878203c9659f2a26ae394656b3147963324c61fa3832f15/work/etcd)
</code></pre>

可以看出来，挂载的目录实际上是两个rkt镜像。 
<pre><code>[root@localhost systemd]# rkt image list
KEY                                                                     APPNAME                         IMPORTTIME                              LATEST
sha512-1eba37d9b344b33d272181e176da111ef2fdd4958b88ba4071e56db9ac07cf62 coreos.com/etcd:v2.0.4          2015-08-31 21:48:42.644 -0400 EDT       false
sha512-91e98d7f1679a097c878203c9659f2a26ae394656b3147963324c61fa3832f15 coreos.com/etcd:v2.0.9          2015-08-31 22:16:00.081 -0400 EDT       false
sha512-ca0bee4ecb888d10cf0816ebe7e16499230ab349bd3126976ab60b9b1db2e120 coreos.com/rkt/stage1:0.8.0     2015-09-01 22:29:04.63 -0400 EDT        false
sha512-05119c0508aae89c99d1d2077725c0192009f2da5b955dcad5631d7626993433 centos:latest                   2015-09-01 22:30:36.366 -0400 EDT       true
sha512-ddff10a5cf165fc34d66a70542edbcd6eda23144e6259cd2f06ad503625fccb6 coreos.com/rkt/stage1:0.8.0     2015-09-06 03:12:25.397 -0400 EDT       false
</code></pre>

#### 试着手工运行  
<pre><code>[root@localhost 8d4ce168-6825-4fbb-b52b-738a3c891a9d]# ./stage1/rootfs/lkvm run --name rkt-8d4ce168-6825-4fbb-b52b-738a3c891a9d-manual2 --no-dhcp --cpu 1 --mem 128 --console=virtio --kernel stage1/rootfs/bzImage --disk stage1/rootfs --params "console=hvc0 init=/usr/lib/systemd/systemd no_timer_check noreplace-smp systemd.default_standard_error=journal+console systemd.default_standard_output=journal+console ip=172.16.28.5::172.16.28.4:255.255.255.254::eth0::: tsc=reliable MACHINEID=8d4ce168-6825-4fbb-b52b-738a3c891a9d quiet"
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


