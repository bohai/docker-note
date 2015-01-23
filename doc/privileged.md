# privileged参数  
<pre><code>
$ docker help run 
...
--privileged=false         Give extended privileges to this container
...
</code></pre>
大约在0.6版，privileged被引入docker。   
使用该参数，container内的root拥有真正的root权限。   
否则，container内的root只是外部的一个普通用户权限。  
### 未设置privileged启动的容器：   
<pre><code>
[root@localhost ~]# docker run -t -i centos:latest bash
[root@65acccbba42f /]# ls /dev
console  fd  full  fuse  kcore  null  ptmx  pts  random  shm  stderr  stdin  stdout  tty  urandom  zero
</code></pre>
### 设置privileged启动的容器：   
<pre><code>
[root@localhost ~]# docker run -t -i --privileged centos:latest bash
[root@c39330902b45 /]# ls /dev/
autofs           dm-1  hidraw0       loop1               null    ptp3    sg0  shm       tty10  tty19  tty27  tty35  tty43  tty51  tty6   ttyS1    usbmon3  vcs5   vfio
bsg              dm-2  hidraw1       loop2               nvram   pts     sg1  snapshot  tty11  tty2   tty28  tty36  tty44  tty52  tty60  ttyS2    usbmon4  vcs6   vga_arbiter
btrfs-control    dm-3  hpet          loop3               oldmem  random  sg2  snd       tty12  tty20  tty29  tty37  tty45  tty53  tty61  ttyS3    usbmon5  vcsa   vhost-net
bus              dm-4  input         mapper              port    raw     sg3  stderr    tty13  tty21  tty3   tty38  tty46  tty54  tty62  uhid     usbmon6  vcsa1  watchdog
console          dm-5  kcore         mcelog              ppp     rtc0    sg4  stdin     tty14  tty22  tty30  tty39  tty47  tty55  tty63  uinput   vcs      vcsa2  watchdog0
cpu              dm-6  kmsg          mem                 ptmx    sda     sg5  stdout    tty15  tty23  tty31  tty4   tty48  tty56  tty7   urandom  vcs1     vcsa3  zero
cpu_dma_latency  fd    kvm           net                 ptp0    sda1    sg6  tty       tty16  tty24  tty32  tty40  tty49  tty57  tty8   usbmon0  vcs2     vcsa4
crash            full  loop-control  network_latency     ptp1    sda2    sg7  tty0      tty17  tty25  tty33  tty41  tty5   tty58  tty9   usbmon1  vcs3     vcsa5
dm-0             fuse  loop0         network_throughput  ptp2    sda3    sg8  tty1      tty18  tty26  tty34  tty42  tty50  tty59  ttyS0  usbmon2  vcs4     vcsa6
</code></pre>


