【Docker官方】
1. docker 1.5.0rc发布
2015.1.23 Docker 1.5 rc1发布。
新特性摘录：
支持新版registry API

加速“docker push”（针对images的多数层在仓库中已经存在的情况）

支持以下新的事件，如“OOM”, ‘exec_create’, and ‘exec_start' 

支持IPv6
支持使用host的pid namespace，`--pid=host` flag 
支持docker容器root分区只读,`--read-only`  flag
支持限制容器总的内存使用，-`--memory-swap` flag 

参考：
https://groups.google.com/forum/#!topic/docker-dev/nzKREJKqxe4


【业界动态】

1. Docker项目运营架构变化

Docker最近在项目运营架构上作出了一些变化，已适应自身的快速发展。

根据数据统计，在2014年，docker项目的贡献者有740人之多，共计5000个pull request，其中50%以上是非docker员工提交的。
现在已经有了20000多个相关的docker项目，85000个docker应用镜像。

在项目架构中增加了chief architect（关注项目方向）、chief maintainer（关注项目维护）、chief operator（关注社区运营）。

http://www.forbes.com/sites/benkepes/2015/01/28/docker-creates-a-more-robust-docker-project-structure/

2. 使用machine在rackspace云中部署docker容器
machine使用docker新发布的项目。主要目的是部署一台docker host环境。
目前多数公有云厂商(google/aws/azure/rackspace)以及vmware、openstack已经支持machine。
https://developer.rackspace.com/blog/using-docker-machine-to-deploy-your-docker-containers-on-rackspace/

3. 微软提供了第一个官方的docker镜像
微软最近提供给了asp.net 5的官方docker镜像。
https://ahmetalpbalkan.com/blog/making-of-aspnet-docker-image/

4.openstack孵化项目magnum提供了第一版release。
magnum项目为openstack提供容器集群服务。
提供对容器的集中管理服务，通过Gantt进行资源调度。兼容kubernetes。
https://github.com/stackforge/magnum

【技术文章】
1. Docker最佳实践
提出了一些使用docker的最佳实践建议，比如：
	使用安全可信的docker镜像
       确保镜像的层次尽量少
       每个进程一个容器
       不要按照多余的包
	...
http://blog.bigstep.com/big-data-performance/docker-best-practices/

2. SDN、容器、未来的改变
探讨了容器和SDN技术，以及未来的变化。容器远高于虚拟机的部署密度带来对网络的影响。
以及centralized和society两种管理模式。
http://thenewstack.io/sdn-docker-real-changes-ahead/

容器网络技术socketplane
http://aucouranton.com/2015/01/16/docker-virtual-networking-with-socketplane-io/

3.讲了一家创业公司将业务迁移到docker上的过程。
以及其中遇到的困难，最终带来的收益。
http://dockerone.com/article/184

4. 在docker中运行GUI程序以及桌面
http://dockerone.com/article/184

5. fuel中应用docker容器技术
fuel是mirantis开发的openstack部署工具，Mirantis是目前openstack最成功的集成商之一。
从fuel5.1开始，开始使用docker进行fuel组件的部署。
提升了组件开发、部署、升级的效率。
https://www.mirantis.com/blog/why-fuel-runs-on-docker/

6. 大量的使用docker部署应用的实践案例...
如：
部署java应用
https://www.rallydev.com/community/engineering/deploying-java-apps-docker-and-armada
部署LAMP
http://www.emergingafrican.com/2015/01/building-simple-lamp-application-using.html
部署Postgresql
https://osxdominion.wordpress.com/2015/01/25/customizing-postgres-in-docker/
部署rails
http://dev.chaione.com/rapid-rails-setup-with-docker-and-fig/
