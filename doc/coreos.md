<pre><code>
qemu环境下启动coreos虚拟机：
1. 下载镜像
2. ssh-keygen产生key
3. 运行命令./coreos_production_qemu.sh --nographic
4. 使用ssh -l core -p 2222 localhost 进入虚拟机

双分区技术：
core@coreos_production_qemu-766-4-0 ~ $ sudo parted /dev/vda
GNU Parted 3.2
Using /dev/vda
Welcome to GNU Parted! Type 'help' to view a list of commands.

(parted) print list
Model: Virtio Block Device (virtblk)
Disk /dev/vda: 9116MB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags: pmbr_boot

Number  Start   End     Size    File system  Name        Flags
 1      2097kB  136MB   134MB   fat16        EFI-SYSTEM  boot, legacy_boot, esp
 2      136MB   138MB   2097kB               BIOS-BOOT   bios_grub
 3      138MB   1212MB  1074MB  ext2         USR-A
 4      1212MB  2286MB  1074MB               USR-B
 6      2286MB  2420MB  134MB   ext4         OEM
 7      2420MB  2487MB  67.1MB               OEM-CONFIG
 9      2487MB  9114MB  6627MB  ext4         ROOT


core@coreos_production_qemu-766-4-0 ~ $ df -h
Filesystem      Size  Used Avail Use% Mounted on
devtmpfs        485M     0  485M   0% /dev
tmpfs           498M     0  498M   0% /dev/shm
tmpfs           498M  260K  497M   1% /run
tmpfs           498M     0  498M   0% /sys/fs/cgroup
/dev/vda9       6.0G   34M  5.6G   1% /
/dev/vda3       985M  390M  545M  42% /usr
/dev/vda1       128M   32M   97M  25% /boot
tmpfs           498M     0  498M   0% /media
tmpfs           498M     0  498M   0% /tmp
config-2         20G  8.0K   20G   1% /media/configvirtfs
/dev/vda6       108M   52K   99M   1% /usr/share/oem

四大组件：
etcd
fleet
kubernetes
flannel
</code></pre>
