参考：
https://github.com/docker/docker/blob/bc684fae642dbf585215b9518f469634a52a5524/daemon/graphdriver/devmapper/README.md

1. docker的元数据在哪里存放？
<pre><code>
[root@centos Desktop]# ls /var/lib/docker/
containers  devicemapper  execdriver  graph  init  linkgraph.db  repositories-devicemapper  volumes
</code></pre>

1.1 元数据目录  
containers中存放了容器的配置信息。  
devicemapper中存放的容器的dm信息。    
graph中存放的镜像的树形关系信息。  
repository-devicemmapper中存放了镜像的dm信息。  


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
[root@centos Desktop]# lsblk
NAME                                 MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
loop3                                  7:3    0    10G  0 loop 
loop4                                  7:4    0     1G  0 loop 
loop5                                  7:5    0     1G  0 loop 
└─docker-253:0-2891886-pool (dm-3)   253:3    0     4G  0 dm   
  ├─docker-253:0-2891886-base (dm-4) 253:4    0    10G  0 dm   
  └─docker-253:0-2891886-ec216e2e5a4f2bca20bd942905ed23aaa5a7bb1198d47222c2bad1c02ac1e53f (dm-5)
                                     253:5    0    10G  0 dm   /var/lib/docker/devicemapper/mnt/ec216e2e5a4f2bca2
loop6                                  7:6    0     4G  0 loop 
└─docker-253:0-2891886-pool (dm-3)   253:3    0     4G  0 dm   
  ├─docker-253:0-2891886-base (dm-4) 253:4    0    10G  0 dm   
  └─docker-253:0-2891886-ec216e2e5a4f2bca20bd942905ed23aaa5a7bb1198d47222c2bad1c02ac1e53f (dm-5)
                                     253:5    0    10G  0 dm   /var/lib/docker/devicemapper/mnt/ec216e2e5a4f2bca2
sda                                    8:0    0 465.8G  0 disk 
├─sda1                                 8:1    0   500M  0 part /boot
└─sda2                                 8:2    0 465.3G  0 part 
  ├─vg_centos-lv_root (dm-0)         253:0    0    50G  0 lvm  /
  ├─vg_centos-lv_swap (dm-1)         253:1    0   3.7G  0 lvm  [SWAP]
  └─vg_centos-lv_home (dm-2)         253:2    0 411.6G  0 lvm  /home
sr0                                   11:0    1  1024M  0 rom  
[root@centos Desktop]# losetup -a
/dev/loop3: [fd02]:14 (/home/data.img)
/dev/loop4: [fd02]:15 (/home/metadata.img)
/dev/loop5: [fd02]:16 (/home/metadata2.img)
/dev/loop6: [fd02]:17 (/home/data2.img)
</code></pre>
