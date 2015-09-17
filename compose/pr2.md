2. rm目前不支持-v参数

dev@4d4d37853115:/go/src/github.com/docker/libcompose$ git diff
diff --git a/cli/command/command.go b/cli/command/command.go
index 0844461..98db84f 100644
--- a/cli/command/command.go
+++ b/cli/command/command.go
@@ -169,6 +169,10 @@ func RmCommand(factory app.ProjectFactory) cli.Command {
                                Name:  "force,f",
                                Usage: "Allow deletion of all services",
                        },
+                       cli.BoolFlag{
+                               Name:  "v",
+                               Usage: "Remove volumes associated with containers",
+                       },
                },
        }
 }
@@ -221,5 +225,7 @@ func Populate(context *project.Context, c *cli.Context) {
                context.Timeout = c.Int("timeout")
        } else if c.Command.Name == "kill" {
                context.Signal = c.String("signal")
+       } else if c.Command.Name == "rm" {
+               context.Volume = c.Bool("v")
        }
 }
diff --git a/docker/container.go b/docker/container.go
index 95b4e2b..991bb56 100644
--- a/docker/container.go
+++ b/docker/container.go
@@ -140,7 +140,7 @@ func (c *Container) Delete() error {
                }
        }

-       return c.client.RemoveContainer(container.Id, true, false)
+       return c.client.RemoveContainer(container.Id, true, c.service.context.Volume)
 }

 func (c *Container) Up(imageName string) error {
diff --git a/project/context.go b/project/context.go
index 06c0a09..594922e 100644
--- a/project/context.go
+++ b/project/context.go
@@ -18,6 +18,7 @@ var projectRegexp = regexp.MustCompile("[^a-zA-Z0-9_.-]")
 type Context struct {
        Timeout             int
        Log                 bool
+       Volume              bool
        Signal              string
        ComposeFile         string
        ComposeBytes        []byte
