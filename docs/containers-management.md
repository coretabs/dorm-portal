# Containers Management

## What Containers Do We Have?

We have 3 containers:

1. **postgres**: database container.
2. **api**: dormitory system container.
3. **nginx**: nginx container.

## Listing Containers

```
docker ps
```

## Checking Container's Logs

Sometimes your container might fail to start, so you will need to read the logs.

First, you need to list all containers with `-a` flag (or --all). This will show all containers (even stopped ones).

```
docker ps -a
```

Then, simply take the first 4 characters of the container ID and put it into this command

```
docker logs <id>
```

## Going into Container's Shell

If you wanna go inside a container, you can use `docker exec` command. Since we use Alpine Linux, we need to run `/bin/sh`

```
docker exec -it <id> /bin/sh
```

* **-i**: interactive.
* **-t**: tty.

## Stopping All Containers

To stop any container (say a hanging container)

```
cd /var/dormportal/app
docker-compose stop
```

## Rebuild All Containers

```
docker-compose up --force-recreate --build -d
```

## Rebuild a Specific Container

You have to first go into the folder of the dorm portal app

```
cd /var/dormportal/app
```

And, you can rebuild any of the 3 containers we have `postgres`, `api`, and `nginx`

To rebuild the nginx container

```
cd /var/dormportal/app
docker-compose up --force-recreate --build -d nginx
```

## Clean up Space

You can delete docker dangling images by

```
docker rmi $(sudo docker images -f "dangling=true" -q)
```

## Resources Usage

To  display the containers' resource usage

```
docker stats
```