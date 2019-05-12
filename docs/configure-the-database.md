# Configuring the Database

## Getting inside the Django app container

To run commands inside the Django app container you need to get inside that container first

```
docker exec -it $(docker ps -a | grep api | awk '{print $1}') /bin/sh
```

Now you're in the shell of that container.


## Migrating and Seeding Database

The database needs to be seeded before you can enter the website

```
python manage.py migrate
```

There are also required records that need to be seeded into the database

```
python manage.py seed
```

## What Are the Required Records in the Database?

The required records are the 4 basic filters used by the filtering engine:

```
Category (Public/Private)
Allowed people number in one room
Reservation Duration (Spring/Winter/Summer/Full Year)
Price
```

## Adding Admin User

To login into the admin panel which is located at

```
http://dorm.mydomain.com/api/admin/
```

So, to add the admin user run this command

```
echo "from api.engine.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
```

This will add an `admin` user with `admin` password (**do NOT forget to change the credentials later from Django admin**).
