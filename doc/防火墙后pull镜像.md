..  
声明：   
本博客欢迎转发，但请保留原作者信息!   
博客地址：http://blog.csdn.net/halcyonbaby   
新浪微博：@寻觅神迹

内容系本人学习、研究和总结，如有雷同，实属荣幸！   

==================
防火墙后pull镜像
==================
很不幸，公司环境在防火墙后边，pull docker镜像一直需要配置proxy代理。    
1.6之前修改方式，一直是在/etc/sysconfig/docker中增加:      
http_proxy=http://xxx.xxx.xxx.xxx:8080     
今天升级1.7后突然发现不行了。    
查看了下文档，发现1.7配置proxy的方法有所改变。   
需要创建如下文件：    
/etc/systemd/system/docker.service.d/http-proxy.conf  
然后增加如下内容：  
<pre><code>
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:80/"
</code></pre>
然后运行：  
<pre><code>
systemctl daemon-reload
systemctl restart docker
</code></pre>
    

