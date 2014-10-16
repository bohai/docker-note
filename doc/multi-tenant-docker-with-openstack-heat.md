译自：http://techs.enovance.com/7104/multi-tenant-docker-with-openstack-heat

Heat是openstack的编排工具，也是通过模板与API交互的系统。Heat已经支持Docker一段时间了，
网上有很多使用的范例。大多数要求Docker部署在你的Heat节点上，所有的用户可以使用。
在学校，我们考虑如何使用安装了docker的nova servers，通过remote API访问他们。
这种方式我们获得一个租户拥有全部控制权的Docker实例。

当探索这些能力，我发现Docker有一些激动人心的特性，可以让template的说明更加优雅。
我写了一个patch使用他们。下边的例子基于此，好消息是最近它将合入heat代码。
你需要打开你的heat环境中的docker插件。

主要解决的问题是，当你使用模板部署
