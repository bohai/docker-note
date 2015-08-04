..  
声明：   
本博客欢迎转发，但请保留原作者信息!   
博客地址：http://blog.csdn.net/halcyonbaby   
新浪微博：寻觅神迹

内容系本人学习、研究和总结，如有雷同，实属荣幸！   

====================================
Flocker初探（2）
====================================
##### Docker的Plugin机制  
Flocker目前采用了Docker的plugin机制，从而与Docker对接。这里先总结下Docker的Plugin
机制。  
Docker1.7开始以experiment特性的方式提供了volume/network插件机制。     
volume插件机制，主要便于第三方的存储管理能够与docker对接，从而为有状态的应用提供
（比如database、key-value store）数据卷。  

用户使用方法如下：
<pre><code>$ docker run -v volume_name:/data --volume-driver=flocker your_stateful_container
</code></pre>

Driver需要实现以下接口：  
<pre><code>/VolumeDriver.Create
/VolumeDriver.Remove
/VolumeDriver.Mount
/VolumeDriver.Path
/VolumeDriver.Unmount
</code></pre>

Plugin还需要一个handshake API。在Docker daemon初次使用时，会通过该API激活Plugin。
<pre><code>/Plugin.Activate
</code></pre>

Plugin发现：  
Plugin目录下会有如下三种文件：
<pre><code>.sock  unix socket file
.spec  文本文件，包含一个URL，例如“unix：///other.sock"
.json  文本文件，包含一个json定义。
</code></pre>
.sock文件通常在/run/docker/plugins下放置，spec、json文件则在/etc/docker/plugins或者
/usr/lib/docker/plugins下。  
Docker会先尝试在/run/docker/plugins下查找sock文件，如果找不到则会在/etd/docker/plugins
或者/usr/lib/docker/plugins下找spec、json文件。  

json文件的例子：
<pre><code>{
  "Name": "plugin-example",
  "Addr": "https://example.com/docker/plugin",
  "TLSConfig": {
    "InsecureSkipVerify": false,
    "CAFile": "/usr/shared/docker/certs/example-ca.pem",
    "CertFile": "/usr/shared/docker/certs/example-cert.pem",
    "KeyFile": "/usr/shared/docker/certs/example-key.pem",
  }
}
</code></pre>

参考：   
https://github.com/docker/docker/tree/master/docs/extend  
##### Flocker的Docker plugin实现   
![Flocker_docker_plugin](https://docs.clusterhq.com/en/1.0.3/_images/docker-plugin-platform-architecture.png)
如图是与容器配合的Flocker架构。Flocker volume manager由Control service和Flocker agent组成，由Docker触发进行控制。

Docker用户可以这样使用：  
<pre><code>docker run -v name:path --volume-driver=flocker</code></pre>

Flocker的插件也很简单，总共不过200行。   
https://github.com/ClusterHQ/flocker-docker-plugin/blob/master/flockerdockerplugin
<pre><code>"""
### flockerdockerplugin.tac
Create the handler that will deal with incoming requests
"""
def getAdapter():
    root = resource.Resource()
    root.putChild("Plugin.Activate", HandshakeResource())
    root.putChild("VolumeDriver.Create", CreateResource())
    root.putChild("VolumeDriver.Remove", RemoveResource())
    root.putChild("VolumeDriver.Path", PathResource())
    root.putChild("VolumeDriver.Mount", MountResource())
    root.putChild("VolumeDriver.Unmount", UnmountResource())

    site = server.Site(root)
    return site
</code></pre>
##### 其他  
看完之后，感觉nova-docker未来也可以考虑使用类似于Flocker的方式与Cinder对接。  
从而为Docker提供丰富的存储能力。 
唯一欠缺的是，目前Docker不支持运行时挂卷、卸卷操作。    
