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


