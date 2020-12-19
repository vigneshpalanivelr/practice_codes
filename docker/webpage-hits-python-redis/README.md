# Original Repo
`git clone https://github.com/rustudorcalin/hit-counter.git`

# Build, Start and Link Docker Containers
```
cd ~/practice_codes/docker/webpage-hits-python-redis/python2
docker build -t python-app .

cd ~/practice_codes/docker/webpage-hits-python-redis/redis-ld
docker build -t redis-ld .

docker run --name dbs-app-redis                                           -d redis-ld
docker run --name web-app-python -p 80:5000 --link dbs-app-redis:redis-lb -d python-app

curl localhost
```

# Docker Compose
```
cd ~/practice_codes/docker/webpage-hits-python-redis/docker-compose
docker-compose up -d
docker-compose ps

curl localhost
```
