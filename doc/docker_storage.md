参考：
https://github.com/docker/docker/blob/bc684fae642dbf585215b9518f469634a52a5524/daemon/graphdriver/devmapper/README.md

1. docker的元数据在哪里存放？
<pre><code>
[root@centos Desktop]# ls /var/lib/docker/
containers  devicemapper  execdriver  graph  init  linkgraph.db  repositories-devicemapper  volumes
</code></pre>

2. docker使用的存储(LVM后端为例）
通过docker -d --storage-opt dm.datadev=/dev/loop6 --storage-opt dm.metadatadev=/dev/loop5指定docker使用的存储池。
<pre><code>
[root@centos Desktop]# docker info 
Containers: 2
Images: 3
Storage Driver: devicemapper
 Pool Name: docker-253:0-2891886-pool
 Data file: /var/lib/docker/devicemapper/devicemapper/data
 Metadata file: /var/lib/docker/devicemapper/devicemapper/metadata
 Data Space Used: 2735.9 Mb
 Data Space Total: 4096.0 Mb
 Metadata Space Used: 2.1 Mb
 Metadata Space Total: 1024.0 Mb
Execution Driver: native-0.2
Kernel Version: 2.6.32-431.23.3.el6.x86_64
[root@centos Desktop]# dmsetup status
docker-253:0-2891886-pool: 0 8388608 thin-pool 32 542/262144 43775/65536 - rw discard_passdown queue_if_no_space 
docker-253:0-2891886-base: 0 20971520 thin 596992 20971519
[root@centos Desktop]# docker info 
Containers: 2
Images: 3
Storage Driver: devicemapper
 Pool Name: docker-253:0-2891886-pool
 Data file: /var/lib/docker/devicemapper/devicemapper/data
 Metadata file: /var/lib/docker/devicemapper/devicemapper/metadata
 Data Space Used: 2735.9 Mb
 Data Space Total: 4096.0 Mb
 Metadata Space Used: 2.1 Mb
 Metadata Space Total: 1024.0 Mb
Execution Driver: native-0.2
Kernel Version: 2.6.32-431.23.3.el6.x86_64
[root@centos Desktop]# dmsetup status
docker-253:0-2891886-pool: 0 8388608 thin-pool 32 542/262144 43775/65536 - rw discard_passdown queue_if_no_space 
vg_centos-lv_home: 0 863117312 linear 
vg_centos-lv_swap: 0 7766016 linear 
vg_centos-lv_root: 0 104857600 linear 
docker-253:0-2891886-ec216e2e5a4f2bca20bd942905ed23aaa5a7bb1198d47222c2bad1c02ac1e53f: 0 20971520 thin 3200000 20971519
docker-253:0-2891886-base: 0 20971520 thin 596992 20971519
[root@centos Desktop]# docker info 
Containers: 2
Images: 3
Storage Driver: devicemapper
 Pool Name: docker-253:0-2891886-pool
 Data file: /var/lib/docker/devicemapper/devicemapper/data
 Metadata file: /var/lib/docker/devicemapper/devicemapper/metadata
 Data Space Used: 2735.9 Mb
 Data Space Total: 4096.0 Mb
 Metadata Space Used: 2.1 Mb
 Metadata Space Total: 1024.0 Mb
Execution Driver: native-0.2
Kernel Version: 2.6.32-431.23.3.el6.x86_64
[root@centos Desktop]# dmsetup status
docker-253:0-2891886-pool: 0 8388608 thin-pool 32 542/262144 43775/65536 - rw discard_passdown queue_if_no_space 
vg_centos-lv_home: 0 863117312 linear 
vg_centos-lv_swap: 0 7766016 linear 
vg_centos-lv_root: 0 104857600 linear 
docker-253:0-2891886-ec216e2e5a4f2bca20bd942905ed23aaa5a7bb1198d47222c2bad1c02ac1e53f: 0 20971520 thin 3200000 20971519
docker-253:0-2891886-base: 0 20971520 thin 596992 20971519
</code></pre>
