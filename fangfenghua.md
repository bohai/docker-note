Docker仓库创建：
docker pull registry
 docker run -d --name registry-instance -e SEARCH_BACKEND=sqlalchemy  -e SETTINGS_FLAVOR=local -e REGISTRY_PORT=5010 -e GUNICORN_OPTS=["--preload"]  -p 5010:5010 registry:latest

Docker仓库UI：
docker pull konradkleine/docker-registry-frontend
docker run -d -e ENV_DOCKER_REGISTRY_HOST=186.100.25.138 -e ENV_DOCKER_REGISTRY_PORT=5010 -p 8083:80 --name front konradkleine/docker-registry-frontend
