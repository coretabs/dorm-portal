Upgrading the System
---

Since we use git, upgrading the system is just a matter of pulling the repository & rebuilding the container

```
cd /var/dormportal/app
git pull
docker-compose up --force-recreate --build -d
```