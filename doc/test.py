import docker
c = docker.Client()
print docker.version
print len(c.containers())
