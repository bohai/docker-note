Shopify是一个电子商务平台，提供专业的网上店面。目前的客户超过12万，包括GE、特斯拉汽车、GitHub等。作为首家市值超过10亿美元的加拿大网络公司，Shopify在欧美市场的影响力也与日俱增。Shopify是一个大型的Ruby on Rails应用，其产品服务器能通过给1700个处理核心和6TB RAM分配任务来完成每秒处理8000多个请求。Shopify在其博客上分享了系列内容来介绍他们的Docker使用经验。

###Shopify容器化容器的一些经验
+ 使用thin容器（即每个容器仅运行一个单一的服务）
+ 什么应用需要容器化？100法则
    + 需要大量实例运行，还是需要1台服务器上提供服务就够了
+ 日志索引 
    + 尽量不修改应用日志行为
    + 构建后台日志处理容器
        + 订阅docker事件
        + 配置日志索引控制容器
        + 容器销毁时，移除索引指令
+ 统计
    + 使用statsD和DataDog进行多层次运行时数据收集
+ 容器化规则
    + ？？（没太明白，是否有参考性）
+ 调试
    + gdb/strace/proc等传统调试方法仍然适用
    + nsenter、nsinit工具
+ 进程层次
    + pid=1的init管理程序（允许和监控工具，秘密管控，服务发现紧密集成，允许我们进行细粒度的健康检查。）
    + pid=2的ppidshim进程（负责启动应用）
+ signals
    + 确保应用按照规范进行信号处理（某些应用并不按规则，比如Resque，使用SIGQUIT来正常关闭，而使用SIGTERM来紧急关闭。）
+ 主机名
    + 主机名最好与容器名一致。便于定位问题。
+ 注册与部署  
    + github hook触发构建
    + nginx反向代理docker  registry

注：
1. http://www.shopify.com/technology/15934308-docker-at-shopify-how-we-built-containers-that-power-over-100-000-online-shops  
2. http://dockerone.com/article/172  
