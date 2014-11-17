### nova-docker安装  
工作原因，尝试了下nova-docker这个插件。目前该项目还在孵化阶段，还未进入oepnstack正式项目。  
##### 安装过程
1. devstack安装openstack环境（注意rpm源和pypi源尽量选用快的，另外某些源可能缺包。比如osolo.concurrency的python库在aliyun的源上就没有）
2. 安装nova-docker（git clone项目，python setup.py install安装）
3. 配置nova.conf（compute driver使用docker driver，firewall driver不能使用libvirt的firewall driver,要用默认的）
4. 上传docker镜像(注意，镜像名在docker和glance上必须保持一致）
<pre><core>docker save tutum/wordpress | glance image-create --is-public=True --container-format=docker --disk-format=raw --name tutum/wordpress
</code></pre>
5. 重启nova-compute/glance-api  
##### 碰到的坑  
1. /run/docker.sock要设置为stack用户可以访问，nova.conf中设置host_url为/run/docker.sock。
2. 需要使用tutum/wordpress这种设置了内部服务的docker镜像。否则会创建容器失败。我尝试了在image参数中增加命令行命令，当时没有成功。
3. docker.inspect_image在很多时候会抛出API error。感觉是代码错误，需要进一步确认。
##### nova-docker的功能情况
1. 支持创建，删除，reboot，log查看，软重启，pause，unpause
2. 支持创建快照（但是快照创建失败。docker images可以看到创建的镜像残留，但是glance上没有）
3. 支持挂载浮动IP。
未完...待续
