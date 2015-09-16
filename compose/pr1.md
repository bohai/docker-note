1. 问题，未检查不存在的服务。

dev@ca4610fc956d:/go/src/github.com/docker/libcompose/cli/main$ git diff
diff --git a/project/project.go b/project/project.go
index d01cefd..0a8bf99 100644
--- a/project/project.go
+++ b/project/project.go
@@ -305,6 +305,11 @@ func (p *Project) traverse(selected map[string]bool, wrappers map[string]*servic

        launched := map[string]bool{}

+       for s, _ := range selected {
+               if wrappers[s] == nil {
+                       return errors.New("No such service: " + s)
+               }
+       }
        for _, wrapper := range wrappers {
                p.startService(wrappers, []string{}, selected, launched, wrapper, action, cycleAction)
        }

