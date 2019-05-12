# VPS Initial Config

## Required Infrastructure

* Server with at least 1GB RAM and 20GB HDD (**recommended specs: 2GB RAM and 40GB HDD**).
* Transactional email service (like mailgun or sendgrid).
* Domain name.
* TLS/SSL certificate (for HTTPS support).

## Connect to Server (SSH)

If you are on Windows, you can use `Git Bash` to follow along:

```
ssh -i ssh_key.pem user@yourserver.domain.com
```

* `ssh_key.pem` is the SSH key file required to connect to the server.
* `user` is the username.
* `yourserver.domain.com` is the server DNS.

Then be the root user

```
sudo -i
```

* I will assume you know what you're doing on your server, and you will **create a specific user with the right permissions**. [You can watch this video for more info.](https://www.youtube.com/watch?v=LbJK48gvXcA&index=4&t=0s&list=PLQlWzK5tU-gDyxC1JTpyC2avvJlt3hrIh)

## Install git

```
apt install git-all
```

## Install Docker

Docker is a platform to develop, deploy, and run applications inside containers. This video gives a nice visual idea about Docker:

https://www.youtube.com/watch?v=YFl2mCHdv24

To install Docker, just simply run this command:

```
wget -qO- https://get.docker.com/ | sh
```

## Install docker-compose

docker-compose is a tool to orchestrate multiple apps in a simple manner, this guide walks you through the basics of docker-compose:

https://www.youtube.com/watch?v=Qw9zlE3t8Ko

You should see the docker-compose version after running these commands

```
apt install curl
curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
docker-compose --version
```