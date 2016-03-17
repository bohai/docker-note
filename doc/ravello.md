..  
声明：   
本博客欢迎转发，但请保留原作者信息!   
博客地址：http://blog.csdn.net/halcyonbaby   
新浪微博：[@寻觅神迹]( www.weibo.com/u/2230330930)

内容系本人学习、研究和总结，如有雷同，实属荣幸！   

-----
### ravello的嵌套虚拟化技术
> 猎云网2月24日报道（编译：田小雪）
>
> Oracle于今日宣布其已正式收购初创企业Ravello Systems。该创企专门研发各种工具以便企业在公共云环境中进行运营工作。虽然Oracle官方并没有披露这笔交易的具体细节，但是有消息来源表示，Oracle出的收购价为5亿美元。

Ravello是个overlay云的提供商，主要在AWS/GCE之上提供运云服务。  
HVX是Revllo的一整套方案（基于高性能嵌套虚拟化/SDN/存储overlay技术），如下图：  

![hvx architecture](https://www.ravellosystems.com/sites/all/themes/ravello/images/new-images/technology/overview.png)

HVX目前的主要面对场景是：
1. 开发/测试场景  
2. 教育培训  
3. openstack实验环境  

### nested-virtualization  
嵌套虚拟化引擎，如下图：  
![nested-virtualization](https://www.ravellosystems.com/sites/all/themes/ravello/images/new-images/technology/hvx-1.png)  







