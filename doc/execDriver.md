### Docker driver指定方式
<pre><code>
[root@localhost temp]# docker help daemon

Usage:  docker daemon [OPTIONS]

Enable daemon mode

...
  -e, --exec-driver=native             Exec driver to use
...
</code></pre>

### Docker的execDriver机制
Docker架构图：  
![docker](http://www.sel.zju.edu.cn/wp-content/uploads/2014/12/docker-1-10-1.jpg)

可以看出，execDriver是插件机制。   
对应代码在docker/deamon/execdriver下，可以看出来目前有lxc、native两种driver。  
未来还会有windows driver。  

代码路径为：
docker/docker.go(func main)->docker/daemon.go(func handleGlobalDaemonFlag)->daemon/daemon.go(func newDaemon)   
在newDaemon中为结构Daemon的execDriver初始化对应的driver（根据-e的参数指定）。  

### execDriver的接口一览
<pre><code>
 70 type Driver interface {
 71     // Run executes the process, blocks until the process exits and returns
 72     // the exit code. It's the last stage on Docker side for running a container.
 73     Run(c *Command, pipes *Pipes, hooks Hooks) (ExitStatus, error)
 74
 75     // Exec executes the process in an existing container, blocks until the
 76     // process exits and returns the exit code.
 77     Exec(c *Command, processConfig *ProcessConfig, pipes *Pipes, hooks Hooks) (int, error)
 78
 79     // Kill sends signals to process in container.
 80     Kill(c *Command, sig int) error
 81
 82     // Pause pauses a container.
 83     Pause(c *Command) error
 84
 85     // Unpause unpauses a container.
 86     Unpause(c *Command) error
 87
 88     // Name returns the name of the driver.
 89     Name() string
 90
 91     // Info returns the configuration stored in the driver struct,
 92     // "temporary" hack (until we move state from core to plugins).
 93     Info(id string) Info
 94
 95     // GetPidsForContainer returns a list of pid for the processes running in a container.
 96     GetPidsForContainer(id string) ([]int, error)
 97
 98     // Terminate kills a container by sending signal SIGKILL.
 99     Terminate(c *Command) error
100
101     // Clean removes all traces of container exec.
102     Clean(id string) error
103
104     // Stats returns resource stats for a running container
105     Stats(id string) (*ResourceStats, error)
106
107     // SupportsHooks refers to the driver capability to exploit pre/post hook functionality
108     SupportsHooks() bool
109 }
</code></pre>

### execDriver目前被用到的接口
<pre><code>
daemon/daemon.go:               daemon.execDriver.Terminate(cmd)
daemon/daemon.go:       base.ExecDriver = daemon.execDriver.Name()
daemon/daemon.go:       return daemon.execDriver.Run(c.command, pipes, hooks)
daemon/daemon.go:       return daemon.execDriver.Kill(c.command, sig)
daemon/daemon.go:       return daemon.execDriver.Stats(c.ID)
daemon/container_unix.go:               if !c.daemon.execDriver.SupportsHooks() || c.hostConfig.NetworkMode.IsHost() {
daemon/container_unix.go:       } else if container.daemon.execDriver.SupportsHooks() {
daemon/container.go:    if err := container.daemon.execDriver.Pause(container.command); err != nil {
daemon/container.go:    if err := container.daemon.execDriver.Unpause(container.command); err != nil {
daemon/exec.go: if err := checkExecSupport(d.execDriver.Name()); err != nil {
daemon/exec.go: exitStatus, err := d.execDriver.Exec(c.command, ExecConfig.ProcessConfig, pipes, hooks)
daemon/delete.go:       if err = daemon.execDriver.Clean(container.ID); err != nil {
</code></pre>

### 写一个自己的execDriver  
<pre><code>
[root@localhost cvm]# cat driver.go
package cvm

import (
        "fmt"
        "sync"
        "time"

        sysinfo "github.com/docker/docker/pkg/system"
        "github.com/docker/docker/daemon/execdriver"
        "github.com/opencontainers/runc/libcontainer"
)

// Define constants for cvm driver
const (
        DriverName = "cvm"
        Version    = "0.1"
)

// Driver contains all information for native driver,
// it implements execdriver.Driver.
type Driver struct {
        root             string
        initPath         string
        activeContainers map[string]libcontainer.Container
        machineMemory    int64
        factory          libcontainer.Factory
        sync.Mutex
}

type info struct {
    ID    string
    driver *Driver
}

// IsRunning is determined by looking for the
// pid file for a container.  If the file exists then the
// container is currently running
func (i *info) IsRunning() bool {
    _, ok := i.driver.activeContainers[i.ID]
    return ok
}


func NewDriver(root, initPath string, options []string) (*Driver, error) {

        meminfo, err := sysinfo.ReadMemInfo()
        if err != nil {
                return nil, err
        }

        return &Driver{
                root:             root,
                initPath:         initPath,
                activeContainers: make(map[string]libcontainer.Container),
                machineMemory:    meminfo.MemTotal,
                factory:          nil,
        }, nil
}

// Run implements the exec driver Driver interface,
// it calls libcontainer APIs to run a container.
func (d *Driver) Run(c *execdriver.Command, pipes *execdriver.Pipes, startCallback execdriver.StartCallback) (execdriver.ExitStatus, error) {
        return execdriver.ExitStatus{ExitCode: 0}, nil
}

func (d *Driver) Kill(c *execdriver.Command, sig int) error {
        return nil
}

func (d *Driver) Pause(c *execdriver.Command) error {
        return nil
}

func (d *Driver) Unpause(c *execdriver.Command) error {
        return nil
}

func (d *Driver) Terminate(c *execdriver.Command) error {
        return nil
}

// Info implements the exec driver Driver interface.
func (d *Driver) Info(id string) execdriver.Info {
        return &info{
                ID:     "id",
                driver: d,
        }
}

// Name implements the exec driver Driver interface.
func (d *Driver) Name() string {
        return fmt.Sprintf("%s-%s", DriverName, Version)
}

// GetPidsForContainer implements the exec driver Driver interface.
func (d *Driver) GetPidsForContainer(id string) ([]int, error) {
        a := []int{1, 2, 3}
        return a, nil

}

// Stats implements the exec driver Driver interface.
func (d *Driver) Stats(id string) (*execdriver.ResourceStats, error) {
        now := time.Now()
        return &execdriver.ResourceStats{
                Stats:       nil,
                Read:        now,
                MemoryLimit: 1000,
        }, nil
}

// SupportsHooks implements the execdriver Driver interface.
// The libcontainer/runC-based native execdriver does exploit the hook mechanism
func (d *Driver) SupportsHooks() bool {
        return true
}

// Clean implements the exec driver Driver interface.
func (d *Driver) Clean(id string) error {
        return nil
}

func (d *Driver) Exec(c *execdriver.Command, processConfig *execdriver.ProcessConfig, pipes *execdriver.Pipes, startCallback execdriver.StartCallback) (int, error) {
        return 0, nil
}
[root@localhost cvm]# cat execdrivers_linux.go
// +build linux

package execdrivers

import (
        "fmt"
        "path"

        "github.com/Sirupsen/logrus"
        "github.com/docker/docker/daemon/execdriver"
        "github.com/docker/docker/daemon/execdriver/lxc"
        "github.com/docker/docker/daemon/execdriver/cvm"
        "github.com/docker/docker/daemon/execdriver/native"
        "github.com/docker/docker/pkg/sysinfo"
)

func NewDriver(name string, options []string, root, libPath, initPath string, sysInfo *sysinfo.SysInfo) (execdriver.Driver, error) {
        switch name {
        case "lxc":
                // we want to give the lxc driver the full docker root because it needs
                // to access and write config and template files in /var/lib/docker/containers/*
                // to be backwards compatible
                logrus.Warn("LXC built-in support is deprecated.")
                return lxc.NewDriver(root, libPath, initPath, sysInfo.AppArmor)
        case "native":
                return native.NewDriver(path.Join(root, "execdriver", "native"), initPath, options)
        case "cvm":
                return cvm.NewDriver(path.Join(root, "execdriver", "cvm"), initPath, options)
        }
        return nil, fmt.Errorf("unknown exec driver %s", name)
}

</code></pre>

### Docker目前的命令归类
可以看出，docker目前并没有动态参数修改类的指令。  
<pre><code>
容器相关：
    attach    Attach to a running container
    cp        Copy files/folders from a container to a HOSTDIR or to STDOUT
    exec      Run a command in a running container
    diff      Inspect changes on a container's filesystem 
    logs      Fetch the logs of a container
    port      List port mappings or a specific mapping for the CONTAINER
    ps        List containers
    rename    Rename a container
    
    create    Create a new container
    kill      Kill a running container
    pause     Pause all processes within a container    
    restart   Restart a running container
    rm        Remove one or more containers
    run       Run a command in a new container
    start     Start one or more stopped containers
    stats     Display a live stream of container(s) resource usage statistics
    stop      Stop a running container
    top       Display the running processes of a container
    unpause   Unpause all processes within a container   
    wait      Block until a container stops, then print its exit code  
镜像相关：
    build     Build an image from a Dockerfile
    commit    Create a new image from a container's changes
    
    login     Register or log in to a Docker registry
    logout    Log out from a Docker registry    
    pull      Pull an image or a repository from a registry
    push      Push an image or a repository to a registry    
    search    Search the Docker Hub for images
    
    import    Import the contents from a tarball to create a filesystem image    
    export    Export a container's filesystem as a tar archive
    load      Load an image from a tar archive or STDIN    
    save      Save an image(s) to a tar archive
    
    rmi       Remove one or more images
    
    history   Show the history of an image    
    images    List images    
    tag       Tag an image into a repository    
其他：
    events    Get real time events from the server
    info      Display system-wide information    
    inspect   Return low-level information on a container or image
    version   Show the Docker version information
</code></pre>

### 编译docker  
其实很简单，我们可以利用现有的docker-dev进行编译：  
1. docker pull docker-dev:1.8.3  
2. docker run -it --name docker-dev docker-dev:1.8.3 /bin/bash  
3. hack/make.sh binary  


