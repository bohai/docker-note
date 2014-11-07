AWS CloudFormation 具备一组 Python 帮助程序脚本，以便您在已作为部分堆栈创建的 Amazon EC2 实例上安装软件并启动服务。
您可以从您的模板中直接调用帮助程序脚本。该脚本可与您在同一模板中定义的资源元数据共同运行。
该帮助程序脚本可在部分堆栈创建进程的 Amazon EC2 实例上运行。

可在 Amazon Linux AMI 最新版本上预先安装该帮助程序脚本。可从 Amazon Linux yum 存储库中获取帮助程序脚本，
与其他 UNIX/Linux AMI 一起使用。当前，AWS CloudFormation 具备以下帮助程序：

cfn-init：用于检索和解释资源元数据、安装程序包、创建文件和启动服务。
cfn-signal：用于发送 CloudFormation WaitCondition 信号的简单包装程序，该程序允许您通过准备就绪的应用程序将堆栈中的
其他资源进行同步。
cfn-get-metadata：包装程序脚本，旨在便于您轻松检索为资源定义的所有元数据或特定密钥路径和资源元数据子树。
cfn-hup：它是一项后台程序，用于检查元数据更新，并在检测出变更时，执行自定义钩子。

这些脚本按照默认方式安装在 /opt/aws/bin 中的最新版本 Amazon Linux AMI 上。针对 Amazon Linux AMI 的先前版本，
可从 Amazon Linux AMI yum 存储库中获取这些脚本在，其亦可通过针对 Linux/Unix 分配的 RPM 获取。
还可利用 Python for Windows 将这些脚本安装在 Microsoft Windows 上。
