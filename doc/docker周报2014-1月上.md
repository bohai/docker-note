Docker官方：
1. docker支持IPV6
https://github.com/docker/docker/pull/8947

2. v1版的docker镜像规格文档
https://github.com/jlhawn/docker/blob/master/image/spec/v1.md

3. docker网络的driver机制（Proposal阶段，未实现）
https://github.com/docker/docker/issues/9983


业界情况：
1.  rocket的App Container Specification
coreos眼中的容器应该具有什么样的能力？
https://github.com/appc/spec/blob/master/SPEC.md

2. openshift 3支持docker
http://www.eweek.com/cloud/red-hat-reimagines-openshift-3-paas-with-docker.html

3. IBM container service
提供了私有仓库（支持上传下载，多租户能力）。
https://cloudleader.wordpress.com/2015/01/11/docker-bluemix-and-the-ibm-container-service/
http://www.ng.bluemix.net/docs/#services/Containers/index.html

4. 腾讯支持docker machine
docker machine是docker去年新发布的一个组件。主要致力于在本地hypervisor上或者云上
配置一个docker host。
目前已经支持在AWS、GCE、Azure、vmware、openstack等上部署一个支持docker的虚拟机环境。
国内腾讯刚刚宣布docker machine支持腾讯云。
http://cloud.yesky.com/451/45027451.shtml


技术文章：
<安全>
1. Docker安全指导
来自GDSSecurity的docker安全指导。该公司是美国一家网络安全公司。
https://github.com/GDSSecurity/Docker-Secure-Deployment-Guidelines

2. Docker镜像并不安全。
讲了一些docker镜像使用上的安全建议，以及目前docker hub安全上存在的问题。

http://linux.cn/article-4702-1.html

如何安全的下载docker镜像。
https://securityblog.redhat.com/2014/12/18/before-you-initiate-a-docker-pull/



<编排>

1. 使用fig进行docker编排
http://blog.arungupta.me/docker-orchestration-fig-techtip67/


<其他>
1.  基于docker的sahara试验
https://software.intel.com/en-us/blogs/2014/12/28/experimenting-with-openstack-sahara-on-docker-containers

2.  docker容器动态挂卷
http://jpetazzo.github.io/2015/01/13/docker-mount-dynamic-volumes/

3. 使用docker部署rails应用的实践
https://www.codeschool.com/blog/2015/01/16/production-deployment-docker/

4. 使用docker7步完成部署mesos
https://medium.com/@gargar454/deploy-a-mesos-cluster-with-7-commands-using-docker-57951e020586

5. 使用docker部署分布式redis系统
http://www.everybodyhertz.co.uk/creating-a-distributed-redis-setup-using-docker/

6. docker网络与pipeworks详解
http://www.infoq.com/cn/articles/docker-network-and-pipework-open-source-explanation-practice

7.2015开篇Docker Meetup：从技术概念到商业实践
joyent、点融网、cisco分享了在公有云、devops、kubernetes、数据库上的应用
http://www.beagledata.com/news/1169.html

8. Gartner认为docker还没有准备在企业中大行其道
http://siliconangle.com/blog/2015/01/13/gartner-docker-not-ready-for-enterprise-prime-time-quite-yet/

9. Docker到底影响了什么
分享了docker对Iaas，Paas，ISV，devops的影响
https://community.emc.com/thread/204521

10. Docker最佳实践
http://blog.bigstep.com/big-data-performance/docker-best-practices/

11. 基于docker的持续集成、持续交付
https://blog.rainforestqa.com/2015-01-15-docker-in-action-from-deployment-to-delivery-part-3-continuous-delivery/


12. 配置openstack在同一台主机上部署容器和虚拟机
通过修改配置，完成在一台主机上同时支持容器和虚拟机两种hypervisor。
这种方式不是openstack官方宣布支持的。
http://blog.oddbit.com/2015/01/17/running-novalibvirt-and-novadocker-on-the-same-host/

13. Cloud Passage支持docker
Cloud Passage是一家软件定义安全类软件提供商。 今日宣称支持docker。
http://www.itbusinessedge.com/blogs/it-unmasked/cloud-passage-moves-to-secure-docker-containers.html
http://www.eweek.com/cloud/cloudpassage-secures-docker-with-cloud-saas.html


14. docker：更有效率的虚拟化
目前70%的服务器在运行虚拟机，传统基于虚拟机的虚拟化有很多优点。同时也存在很多问题。
比如：
由于各种开销，实际上被应用使用到的70%的资源，剩下的30%则由于各种开销消耗掉。
秒级的发放和启动时间。
同样的软件在开发环境运行正常，在生产环境却存在问题。
http://blog.maestrano.com/docker-and-virtualization-became-efficient-part-1/

15. 关于microservice的8个问题
http://blog.xebialabs.com/2014/12/31/8-questions-need-ask-microservices-containers-docker-2015/

16. 基于fig和docker进行geoserver部署
越来越多的应用在尝试使用docker部署。这个例子中使用了fig作为编排工具。
http://kartoza.com/orchestrating-geoserver-with-docker-and-fig/

17. docker已经到了转折点
docker日渐被人接受，目前各大公有云 也已经支持docker。
docker逐步进入大规模实践应用的转折点。
http://room4debate.com/debate/dockers-tipping-point

18. 支持docker的cloud backup
http://www.theregister.co.uk/2015/01/07/asigra_dockerises_cloud_backup/


备注：
Docker每周文章归档
http://blog.docker.com/docker-weekly-archives/

facebook docker首页
https://www.facebook.com/docker.run


