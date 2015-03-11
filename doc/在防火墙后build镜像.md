> 由于各种原因，很多公司设置了防火墙，限制办公环境到外网的接入。这对docker build镜像产生了影响。

在防火墙后build镜像的方法
=========================
修改Dockerfile文件，增加proxy环境变量如下：   
ENV http_proxy http://186.100.100.22:808  
ENV https_proxy http://186.100.100.22:808   

然后就可以愉快的进行容器镜像的build了。


