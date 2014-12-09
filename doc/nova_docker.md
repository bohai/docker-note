### nova-docker现状
nova-docker插件在i版本从nova中移出，作为孵化项目培养。   
当时给出的解释是，希望能更快的进行迭代开发，支持cinder和neutron。并计划在K版本release时重新进入。  

### nova-docker的架构  
目前的架构如下（其中docker registry已经不需要了）  
<img src="https://wiki.openstack.org/w/images/6/6c/Docker-under-the-hood.png" alt="nova_docker" title="nova_docker" width="400" />   


参考：  
http://technodrone.blogspot.com/2014/10/nova-docker-on-juno.html  
