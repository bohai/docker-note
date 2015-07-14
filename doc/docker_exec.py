#!/usr/bin/env python
#coding:utf-8

from docker import Client
import docker

class DockerExec(object):
    def __init__(self):
        self.cl = Client(base_url='unix://var/run/docker.sock')

    def execute(self, container, command, detach=False, interactive=False, tty=False):
        try:
            exec_id = self.cl.exec_create(container, command,  True, True, tty)
            print exec_id
            ret = self.cl.exec_start(exec_id['Id'], detach, tty, False)
            print ret
            ins = self.cl.exec_inspect(exec_id['Id'])
            print ins['ExitCode']
        except docker.errors.APIError as ex:
            raise

if __name__=='__main__':
    client = DockerExec()
    client.execute("bb", "ls -l", False, True, True)


