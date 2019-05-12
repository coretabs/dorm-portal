# Quick Start

## Deployment in 6 Mins

<iframe width="560" height="315"
src="https://www.youtube.com/embed/QFRnuLnEilA" 
frameborder="0" 
allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
allowfullscreen></iframe>

## Cheat Sheet

```
ssh -i ssh_key.pem user@yourserver.domain.com

docker exec -it $(docker ps -a | grep api | awk '{print $1}') /bin/sh
python manage.py migrate

cd /var/academy
git pull
docker-compose up --force-recreate --build -d

sudo docker rmi $(sudo docker images -f "dangling=true" -q)
```