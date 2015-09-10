..  
声明：   
本博客欢迎转发，但请保留原作者信息!   
博客地址：http://blog.csdn.net/halcyonbaby   
新浪微博：[@寻觅神迹]( www.weibo.com/u/2230330930)

内容系本人学习、研究和总结，如有雷同，实属荣幸！   

-----
Cgroup memory详解
---
### 限制范围
所有已经映射页的RSS的内存和page cache内存都在统计范围。
>All mapped anon pages (RSS) and cache pages (Page Cache) are accounted.
Some pages which are never reclaimable and will not be on the LRU
are not accounted. We just account pages under usual VM management.

### 可配置参数 
<pre><code> tasks    		            # attach a task(thread) and show list of threads
 memory.limit_in_bytes		 # set/show limit of memory usage
 memory.soft_limit_in_bytes	 # set/show soft limit of memory usage
 memory.oom_control    	     # set/show oom controls.
</code></pre>

需要说明的是oom_control，默认为0，在内存OOM时动作为kill进程。
如果修改为1，在内存OOM时候进程会被休眠。待内存足够时，会被重新唤醒。

### 程序验证 
测试程序，申请64KB的内存。
<pre><code>[root@localhost ~]# cat testmem.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(void)
{
    void *p= NULL;

    printf("sleep 20s ...\n");
    sleep(20);

    printf("before malloc ...\n");
    p = malloc(sizeof(char)*64*1024);
    memset(p, 1, 64*1024);
    printf("after malloc ...\n");

    sleep(20);

    return 0;
}
</code></pre>
当oom_control为enable(0)时，limit_in_bytes为4K。
由于限制，程序被Kill。
<pre><code>[root@localhost ~]# ./a.out
sleep 20s ...
before malloc ...
Killed
</code></pre>
当oom_control为enable(0)时，limit_in_bytes为4K。
由于超出限制，程序被休眠。
之后调整limit_in_bytes为128K，程序继续运行。
<pre><code>
[root@localhost ~]# ./a.out
sleep 20s ...
before malloc ...
after malloc ...
</code></pre>

### 参考
1. https://lwn.net/Articles/529927/
2. http://183.91.33.12/cache/files.cnblogs.com/files/lisperl/cgroups%E4%BB%8B%E7%BB%8D.pdf?ich_args=1e57d7581dfd5560617250e46746fe18_1_0_0_3_9e8489f777f7683cda7ff9239402bec1b05bb89bea150c1c5a0d4ac6bc8b25c9_5141805d3b5cb1563c44c604795d66a5_1_0&ich_ip=33-7



