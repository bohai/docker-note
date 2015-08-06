..  
声明：   
本博客欢迎转发，但请保留原作者信息!   
博客地址：http://blog.csdn.net/halcyonbaby   
新浪微博：@寻觅神迹

内容系本人学习、研究和总结，如有雷同，实属荣幸！   

----------
### 写一个简单的docker volume Plugin
该插件只是个例子，卷实际上是host上的目录，但是由插件进行管理。  
代码中使用了calavera写的docker volume plugin框架。  
需要完成的只是上章所说的docker volume plugin的5个接口。  
**main.go的代码**
<pre><code>
package main

import (
        "flag"
        "fmt"
        "log"
        "os"
        "path/filepath"
        "sync"

        "github.com/calavera/dkvolume"
)

var (
        root = flag.String("root", "/var/lib/docker/fakevol", "fake volumes root directory")
)

type fakeVolDriver struct {
        root    string
        m       *sync.Mutex
        volumes map[string]string
}

func newFakeVolDriver(root string) fakeVolDriver {
        d := fakeVolDriver{
                root:    root,
                volumes: map[string]string{},
                m:       &sync.Mutex{},
        }
        return d
}

func (d fakeVolDriver) Create(r dkvolume.Request) dkvolume.Response {
        log.Printf("Creating volume %s\n", r.Name)
        d.m.Lock()
        defer d.m.Unlock()
        volPath := filepath.Join(d.root, r.Name)
        if _, err := os.Stat(volPath); os.IsNotExist(err) {
                os.Mkdir(volPath, 0755)
                d.volumes[r.Name] = volPath
        }

        return dkvolume.Response{}
}

func (d fakeVolDriver) Remove(r dkvolume.Request) dkvolume.Response {
        log.Printf("Removing volume %s\n", r.Name)
        d.m.Lock()
        defer d.m.Unlock()
        if _, err := os.Stat(d.volumes[r.Name]); os.IsNotExist(err) {
                os.Remove(d.volumes[r.Name])
                delete(d.volumes, r.Name)
        }

        return dkvolume.Response{}
}

func (d fakeVolDriver) Path(r dkvolume.Request) dkvolume.Response {
        return dkvolume.Response{Mountpoint: d.volumes[r.Name]}
}

func (d fakeVolDriver) Mount(r dkvolume.Request) dkvolume.Response {
        return dkvolume.Response{Mountpoint: d.volumes[r.Name]}
}

func (d fakeVolDriver) Unmount(r dkvolume.Request) dkvolume.Response {
        return dkvolume.Response{}
}

func main() {
        flag.Parse()

        d := newFakeVolDriver(*root)
        h := dkvolume.NewHandler(d)
        fmt.Println(h.ServeUnix("root", "fakeVol"))
}
</code></pre>

**运行、使用plugin管理容器的volume**
<pre><code>
[root@localhost fake-volume]# ./fake-volume
[root@localhost fake-volume]# ls /run/docker/plugins/fakeVol.sock
/run/docker/plugins/fakeVol.sock
[root@localhost temp]# docker5500 run -it --rm  -v test:/test --volume-driver=fakeVol busybox:latest /bin/sh
/ # ls /test/
/ # touch /test/a.txt
/ # echo "hello docker plugin" > /test/a.txt
[root@localhost calavera]# cat /var/lib/docker/fakevol/test/a.txt
hello docker plugin
</code></pre>

备注：   
由于volume plugin是docker的实验特性。因此正式的release中并未包含。需要使用编译了实验特性的版本。   
可以在```https://experimental.docker.com/builds/Linux/x86_64/docker-latest```下载。
