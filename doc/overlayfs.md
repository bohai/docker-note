Overlay文件系统使用方法：  

mount -t overlay overlay -olowerdir=/lower,upperdir=/upper,\
workdir=/work /merged
