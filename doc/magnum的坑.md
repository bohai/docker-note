1. 
bay创建失败，详细查看原因是heat stack创建失败。  
stack创建失败原因是 wait condition创建失败。  

解决办法firewall-cmd 将8000 tcp端口打开。详细参见：  
https://github.com/larsks/heat-kubernetes/issues/13
