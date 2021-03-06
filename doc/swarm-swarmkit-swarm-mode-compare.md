..  
声明：   
本博客欢迎转发，但请保留原作者信息!   
博客地址：http://blog.csdn.net/halcyonbaby   
新浪微博：@寻觅神迹  
原文地址： https://sreeninet.wordpress.com/2016/07/14/comparing-swarm-swarmkit-and-swarm-mode/

本文系个人翻译，错漏之处请见谅。  

====================================
Swarm、SwarmKit、Swarm mode 对比
====================================
Docker1.12的一个重大特性是提供了swarm mode。Docker结合swarm从1.6开始支持容器编排。  
Docker1.12发布前几周，docker还开源了swarmkit，一个用于编排分布式系统的项目。   
这三个项目让人颇为困惑，这篇博客中我和大家一起看下他们的相似之处以及区别。    
我还会拿一个应用作为例子，来比较三者哪个更容易使用。  

Docker swarm mode和swarm存在本质区别，但是却使用了swarm这个易于混淆的名字。  
我觉得docker社区应该考虑换个名字。另外一点同样增加了这个混淆，native swarm会在1.12继续支持，从而提供兼容性。   
这篇Blog中，我们使用“Swarm”表示老的swarm项目，“Swarmkit”表示新开源的swarmkit项目，“SwarmNext”表示docker swarm mode。   

### Swarm, SwarmNext and Swarmkit  
下边是Swarm和SwarmNext的对比：  

Swarm |SwarmNext
---------|----------
Separate from Docker Engine and can run as Container |Integrated inside Docker engine
Needs external KV store like Consul, etcd|No need of separate external KV store
Service model not available|Service model is available. This provides features like scaling, rolling update, service discovery, load balancing and routing mesh
Communication not secure|Both control and data plane is secure
Integrated with machine and compose|Not yet integrated with machine and compose as of release 1.12. Will be integrated in the upcoming releases

下边是SwarmKit与SwarmNext的对比：  

SwarmKit|SwarmNext
--------------|---------------------
Plumbing opensource project|Swarmkit used within SwarmNext and tightly integrated with Docker Engine
Swarmkit needs to built and run separately|Docker 1.12 comes integrated with SwarmNext
No service discovery, load balancing and routing mesh|Service discovery, load balancing and routing mesh available
Use swarmctl CLI|Use regular Docker CLI

### Sample Application   
下边是一个非常简单的应用。该应用时一个高可用的web投票服务，可以通过client访问。       
client的请求会被负载均衡到各个可用的web服务上。     
应用使用overlay网络，我们将使用Swarm、SwarmNext、SwarmKit进行部署。

![vote_web_system](https://sreeninet.files.wordpress.com/2016/07/swarm1.png?w=301&h=162)

#### 前提条件
本文中使用docker-machine0.8.0-rc1 ，docker1.12.0-rc3.   
“smakam/myubuntu” 容器使用的是ubuntu系统，加下一些比如curl的工具来展示负载均衡。     

### 使用Swarm进行部署   
步骤：  
+ 创建KV存储。这里使用consul。  
+ 创建使用consul存储的docker实例。这里使用docker-machine创建。  
+ 创建overlay网络。  
+ 创建投票web系统的多实例以及client单实例。所有的web服务需要使用相同的网络别名，以便可以进行流量的负载均衡。  

创建KV存储：  
```shell     
docker-machine create -d virtualbox mh-keystore  
eval "$(docker-machine env mh-keystore)"  
docker run -d \  
    -p "8500:8500" \  
    -h "consul" \  
    progrium/consul -server -bootstrap  
```  

创建使用KV存储的Docker swarm 实例：    
```shell   
docker-machine create \  
-d virtualbox \  
--swarm --swarm-master \   
--swarm-discovery="consul://$(docker-machine ip mh-keystore):8500" \  
--engine-opt="cluster-store=consul://$(docker-machine ip mh-keystore):8500" \  
--engine-opt="cluster-advertise=eth1:2376" \  
mhs-demo0  

docker-machine create -d virtualbox \  
    --swarm \  
    --swarm-discovery="consul://$(docker-machine ip mh-keystore):8500" \  
    --engine-opt="cluster-store=consul://$(docker-machine ip mh-keystore):8500" \  
    --engine-opt="cluster-advertise=eth1:2376" \  
  mhs-demo1  
```  

创建overlay网络：   
```shell
eval $(docker-machine env --swarm mhs-demo0)  
docker network create --driver overlay overlay1   
```

创建服务：  
两个投票服务的容器，都是用相同网络别名“vote"，从而可以被作为一个服务来访问。  
```shell 
docker run -d --name=vote1 --net=overlay1 --net-alias=vote instavote/vote
docker run -d --name=vote2 --net=overlay1 --net-alias=vote instavote/vote
docker run -ti --name client --net=overlay1 smakam/myubuntu:v4 bash
```

从client容器中访问vote web服务：
```shell 
root@abb7ec6c67fc:/# curl vote  | grep "container ID"
          Processed by container ID a9c05cd4ee15
root@abb7ec6c67fc:/# curl -i vote  | grep "container ID"
          Processed by container ID ce94f38fc958
```

从上边可以看到，请求被均衡到了两个vote web服务。

### 使用SwarmNext进行部署
步骤如下：  
+ 使用docker machine和1.12 RC3的docker创建两个docker实例。其中一个作为master节点，另外一个作为worker节点。
+ 创建overlay网络。
+ 基于overlay网络创建2个副本的web投票服务，1个副本的client服务。

创建两个docker实例：
```shell
docker-machine create -d virtualbox node1
docker-machine create -d virtualbox node2
```

设置node1为master节点： 
```shell
docker swarm init --listen-addr 192.168.99.100:2377
```
node1同时作为woker节点运行。   

设置node2为worker节点：  
```shell  
docker swarm join 192.168.99.100:2377
```

查看云运行的nodes：
```shell
$ docker node ls
ID                           HOSTNAME  MEMBERSHIP  STATUS  AVAILABILITY  MANAGER STATUS
b7jhf7zddv2w2evze1bz44ukx *  node1     Accepted    Ready   Active        Leader
ca4jgzcnyz70ry4h5enh701fv    node2     Accepted    Ready   Active    
```

创建overlay网络：  
```shell 
docker network create --driver overlay overlay1
```

创建服务：
```shell
docker service create --replicas 1 --name client --network overlay1 smakam/myubuntu:v4 ping docker.com
docker service create --name vote --network overlay1 --replicas 2 -p 8080:80 instavote/vote
```

在这个例子中，本不需要把port映射到host上，但是我还是使用了。  
使用docker1.12的routing mesh特性，将8080端口映射到了node1和node2上。

查看运行的服务：
```shell
$ docker service ls
ID            NAME    REPLICAS  IMAGE               COMMAND
2rm1svgfxzzw  client  1/1       smakam/myubuntu:v4  ping docker.com
af6lg0cq66bl  vote    2/2       instavote/vote 
```

从client容器连接web投票系统：
```shell
# curl vote | grep "container ID"
          Processed by container ID c831f88b217f
# curl vote | grep "container ID"
          Processed by container ID fe4cc375291b
```

同样我们看到，client的请求被均衡到了两个web服务容器。   

### 使用SwarmKit进行部署
步骤：  
+ 使用docker-machine创建2node的cluster。Swarm集群虽然可以不适用KV存储。但是overlay网络需要KV存储。所以例子中我会使用KV存储。   
+ 构建swarmkit并把二进制部署到swarm节点。  
+ 创建2个node的swarm集群。  
+ 创建overlay网络以及创建基于overlay网络的服务。  

构建swarmkit：  
这里在Go container中进行swarmkit的编译。  
```shell
git clone https://github.com/docker/swarmkit.git
eval $(docker-machine env swarm-01)
docker run -it --name swarmkitbuilder -v `pwd`/swarmkit:/go/src/github.com/docker/swarmkit golang:1.6 bash
cd /go/src/github.com/docker/swarmkit
make binaries
```

创建基于KV存储的Docker实例：
```shell
docker-machine create \
-d virtualbox \
--engine-opt="cluster-store=consul://$(docker-machine ip mh-keystore):8500" \
--engine-opt="cluster-advertise=eth1:2376" \
swarm-01
docker-machine create -d virtualbox \
--engine-opt="cluster-store=consul://$(docker-machine ip mh-keystore):8500" \
--engine-opt="cluster-advertise=eth1:2376" \
swarm-02
```

拷贝swarmkit到node中：
```shell
docker-machine scp bin/swarmd swarm-01:/tmp
docker-machine scp bin/swarmctl swarm-01:/tmp
docker-machine ssh swarm-01 sudo cp /tmp/swarmd /tmp/swarmctl /usr/local/bin/
docker-machine scp bin/swarmd swarm-02:/tmp
docker-machine scp bin/swarmctl swarm-02:/tmp
docker-machine ssh swarm-02 sudo cp /tmp/swarmd /tmp/swarmctl /usr/local/bin/
```

创建swarm cluster：
```shell
Master:
docker-machine ssh swarm-01
swarmd -d /tmp/swarm-01 \
--listen-control-api /tmp/swarm-01/swarm.sock \
--listen-remote-api 192.168.99.101:4242 \
--hostname swarm-01 &

Worker:
swarmd -d /tmp/swarm-02 \
--hostname swarm-02 \
--listen-remote-api 192.168.99.102:4242 \
--join-addr 192.168.99.101:4242 &
```

创建overlay网络和服务：
```shell
swarmctl network create --driver overlay --name overlay1
swarmctl service create --name vote --network overlay1 --replicas 2 --image instavote/vote
swarmctl service create --name client --network overlay1 --image smakam/myubuntu:v4 --command ping,docker.com
```

查看2node cluster：
```shell
export SWARM_SOCKET=/tmp/swarm-01/swarm.sock
swarmctl node ls

ID                         Name      Membership  Status   Availability  Manager Status
--                         ----      ----------  ------   ------------  --------------
5uh132h0acqebetsom1z1nntm  swarm-01  ACCEPTED    READY    ACTIVE        REACHABLE *
5z8z6gq36maryzrsy0cmk7f51            ACCEPTED    UNKNOWN  ACTIVE  
```

通过client容器连接web投票系统：  
```shell
# curl 10.0.0.3   | grep "container ID"
          Processed by container ID 78a3e9b06b7f
# curl 10.0.0.4   | grep "container ID"
          Processed by container ID 04e02b1731a0
```

因为swarmkit没有负载均衡、服务发现能力，我们使用容器的IP来进行访问。  


### 总结
SwarmNext（docker的swarm mode）相对于之前的swarm是一个重大的改进。将服务对象引入docker中，可以很容易的实现诸如
scaling、rolling update、service discovery、load balance、routing mesh的特性。  
这样swarm可以在特性上更接近于kubernetes。  
在1.12release中，docker支持SwarmNext和Swarm，之前将swarm用于生产环境的用户，可以进行升级。  
SwarmNext目前还不能与compose、stoarge插件很好的集成，但是应该会在之后的版本增加这些能力。  
从长期来说，swarm会被废弃，SwarmNext会成为docker的唯一编排方式。  
将Swarmkit开源，有利于swarmkit的独立开发，以及第三方基于swarmkit开发分布式应用的编排系统。
