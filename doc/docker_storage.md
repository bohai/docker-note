参考：
https://github.com/docker/docker/blob/bc684fae642dbf585215b9518f469634a52a5524/daemon/graphdriver/devmapper/README.md

1. docker的元数据在哪里存放？
<pre><code>
[root@centos Desktop]# ls /var/lib/docker/
containers  devicemapper  execdriver  graph  init  linkgraph.db  repositories-devicemapper  volumes
</code></pre>
2. 元数据目录  
containers中存放了容器的配置信息。  
devicemapper中存放的容器的dm信息。    
graph中存放的镜像的树形关系信息。  
repository-devicemmapper中存放了镜像的dm信息。  
3. docker使用的存储(LVM后端为例）
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
4. 使用NFS共享存储给容器
<pre><code>
[root@centoo65 data]# docker run -i -t -v /nfs/boh/:/nfs/boh/ centos:latest /bin/bash
bash-4.2# ls /nfs/boh/
a.txt
bash-4.2# touch /nfs/boh/b.txt
[root@centoo65 ~]# ls /nfs/boh/
a.txt  b.txt
[root@centoo65 ~]# mount
/dev/sda1 on / type ext4 (rw)
proc on /proc type proc (rw)
sysfs on /sys type sysfs (rw)
devpts on /dev/pts type devpts (rw,gid=5,mode=620)
tmpfs on /dev/shm type tmpfs (rw)
/dev/sda3 on /data type ext4 (rw)
none on /proc/sys/fs/binfmt_misc type binfmt_misc (rw)
sunrpc on /var/lib/nfs/rpc_pipefs type rpc_pipefs (rw)
186.100.8.172:/home/zhang on /nfs type nfs (rw,vers=4,addr=186.100.8.172,clientaddr=186.100.8.138)
</code></pre>
5. 使用共享块设备  
<pre><code>
[root@centoo65 ~]# losetup -a
/dev/loop0: [0801]:6291985 (/dev/loop0)
/dev/loop1: [0801]:6291986 (/dev/loop1)
/dev/loop3: [0803]:16 (/data/floppy.img)
/dev/loop4: [0803]:19 (/data/metadata.img)
[root@centoo65 data]# docker run -i -t --privileged=true -v /dev/loop3:/dev/sdb centos:latest /bin/bash
bash-4.2# mount /dev/sdb /mnt/
bash-4.2# ls -l /mnt/
total 16
drwx------ 2 root root 16384 Oct 20 07:48 lost+found
bash-4.2# touch /mnt/test.txt
[root@centoo65 ~]# mount /dev/loop3  /mnt/
[root@centoo65 ~]# ls -l /mnt/
total 16
drwx------ 2 root root 16384 Oct 20 02:48 lost+found
-rw-r--r-- 1 root root     0 Oct 20 02:49 test.txt
</code></pre>
