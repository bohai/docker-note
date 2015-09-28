dev@f65b297dae93:/go/src/github.com/docker/libcompose$ git diff
diff --git a/cli/app/app.go b/cli/app/app.go
index b07f4ec..a77c12a 100644
--- a/cli/app/app.go
+++ b/cli/app/app.go
@@ -45,13 +45,14 @@ func WithProject(factory ProjectFactory, action ProjectAction) func(context *cli
 // ProjectPs lists the containers.
 func ProjectPs(p *project.Project, c *cli.Context) {
        allInfo := project.InfoSet{}
+       qFlag := c.Bool("q")
        for name := range p.Configs {
                service, err := p.CreateService(name)
                if err != nil {
                        logrus.Fatal(err)
                }

-               info, err := service.Info()
+               info, err := service.Info(qFlag)
                if err != nil {
                        logrus.Fatal(err)
                }
@@ -59,7 +60,7 @@ func ProjectPs(p *project.Project, c *cli.Context) {
                allInfo = append(allInfo, info...)
        }

-       os.Stdout.WriteString(allInfo.String())
+       os.Stdout.WriteString(allInfo.String(!qFlag))
 }

 // ProjectPort prints the public port for a port binding.
diff --git a/cli/command/command.go b/cli/command/command.go
index 0844461..ceedb07 100644
--- a/cli/command/command.go
+++ b/cli/command/command.go
@@ -30,6 +30,12 @@ func PsCommand(factory app.ProjectFactory) cli.Command {
                Name:   "ps",
                Usage:  "List containers",
                Action: app.WithProject(factory, app.ProjectPs),
+               Flags: []cli.Flag{
+                       cli.BoolFlag{
+                               Name:  "q",
+                               Usage: "Only display IDs",
+                       },
+               },
        }
 }

diff --git a/docker/container.go b/docker/container.go
index 95b4e2b..8e3e8d0 100644
--- a/docker/container.go
+++ b/docker/container.go
@@ -47,7 +47,7 @@ func (c *Container) findInfo() (*dockerclient.ContainerInfo, error) {
        return c.client.InspectContainer(container.Id)
 }

-func (c *Container) Info() (project.Info, error) {
+func (c *Container) Info(qFlag bool) (project.Info, error) {
        container, err := c.findExisting()
        if err != nil {
                return nil, err
@@ -55,10 +55,14 @@ func (c *Container) Info() (project.Info, error) {

        result := project.Info{}

-       result = append(result, project.InfoPart{Key: "Name", Value: name(container.Names)})
-       result = append(result, project.InfoPart{Key: "Command", Value: container.Command})
-       result = append(result, project.InfoPart{Key: "State", Value: container.Status})
-       result = append(result, project.InfoPart{Key: "Ports", Value: portString(container.Ports)})
+       if qFlag {
+               result = append(result, project.InfoPart{Key: "Id", Value: container.Id})
+       } else {
+               result = append(result, project.InfoPart{Key: "Name", Value: name(container.Names)})
+               result = append(result, project.InfoPart{Key: "Command", Value: container.Command})
+               result = append(result, project.InfoPart{Key: "State", Value: container.Status})
+               result = append(result, project.InfoPart{Key: "Ports", Value: portString(container.Ports)})
+       }

        return result, nil
 }
diff --git a/docker/service.go b/docker/service.go
index 7d5b1f1..2092466 100644
--- a/docker/service.go
+++ b/docker/service.go
@@ -132,7 +132,7 @@ func (s *Service) Up() error {
        return s.up(imageName, true)
 }

-func (s *Service) Info() (project.InfoSet, error) {
+func (s *Service) Info(qFlag bool) (project.InfoSet, error) {
        result := project.InfoSet{}
        containers, err := s.collectContainers()
        if err != nil {
@@ -140,7 +140,7 @@ func (s *Service) Info() (project.InfoSet, error) {
        }

        for _, c := range containers {
-               if info, err := c.Info(); err != nil {
+               if info, err := c.Info(qFlag); err != nil {
                        return nil, err
                } else {
                        result = append(result, info)
diff --git a/project/info.go b/project/info.go
index 6a5c996..ed799ad 100644
--- a/project/info.go
+++ b/project/info.go
@@ -6,14 +6,14 @@ import (
        "text/tabwriter"
 )

-func (infos InfoSet) String() string {
+func (infos InfoSet) String(titleFlag bool) string {
        //no error checking, none of this should fail
        buffer := bytes.NewBuffer(make([]byte, 0, 1024))
        tabwriter := tabwriter.NewWriter(buffer, 4, 4, 2, ' ', 0)

        first := true
        for _, info := range infos {
-               if first {
+               if first && titleFlag {
                        writeLine(tabwriter, true, info)
                }
                first = false
diff --git a/project/types.go b/project/types.go
index 5c957ac..c27d8ca 100644
--- a/project/types.go
+++ b/project/types.go
@@ -221,7 +221,7 @@ type Project struct {
 }

 type Service interface {
-       Info() (InfoSet, error)
+       Info(qFlag bool) (InfoSet, error)
        Name() string
        Build() error
        Create() error
