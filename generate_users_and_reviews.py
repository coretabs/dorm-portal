from random import randint
from faker import Faker
from api.engine.models import *


fake = Faker()

for _ in range(100):
    name = fake.name().replace(' ', '')
    user = User(first_name=name, username=name, email=f'{name}@gmail.com')
    user.save()
    room_characteristics = RoomCharacteristics.objects.all()[0]
    res = Reservation.create(user=user, room_characteristics=room_characteristics)
    res.save()
    res.update_status(f'{randint(0, 5)}')
    res.save()
    is_lets_review = randint(0, 1)
    if is_lets_review:
        res.create_review(stars=4.5, description='it was a bit good')
