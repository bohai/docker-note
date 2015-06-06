＃获取本机ip
MYIP=`ifconfig eth0 |grep inet |grep netmask |awk '{print $2}'`

#如果没有启动过则启动
docker ps -a |grep registry
if [ $? -ne 0 ];then
    docker run -d --name registry  --restart=always -e SEARCH_BACKEND=sqlalchemy  -e     SETTINGS_FLAVOR=local -e REGISTRY_PORT=5010 -e GUNICORN_OPTS=["--preload"]  -p 5010:5010 registry:latest
fi

docker ps -a |grep registry
if [ $? -ne 0 ];then
 docker run -d --restart=always -e ENV_DOCKER_REGISTRY_HOST=186.100.25.138 -e ENV_DOCKER_REGISTRY_PORT=5010 -p 8083:80 --name front konradkleine/docker-registry-frontend
fi


1 虚拟机中继承此脚本并开机启动
