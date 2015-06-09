参考：　https://github.com/docker/distribution　　　

目前支持存储主要有以下：　

inmemory            使用内存进行存储。主要用于测试、开发目的。   
filesystem          使用本地文件系统的目录。适用于小规模的使用。  

基于具体云存储的仓库。  
s3                  使用amazon S3存储。   
azure               使用Azure的Blob存储。  

rados  适用于中、大规模。基于CEPH。

speedy              京东开源的，基于分布式存储的一种后端。使用与大规模方式的。  
参考：https://github.com/jcloudpub/speedy  

