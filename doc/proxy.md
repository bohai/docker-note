###解决proxy后docker pull镜像的问题

/etc/sysconfig/docker

Adding below line helped me to get docker daemon working behind proxy server:

export HTTP_PROXY="http://<proxy_host>:<proxy_port>"   
export HTTPS_PROXY="http://<proxy_host>:<proxy_port>"   
