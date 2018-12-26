from django.core.management.base import BaseCommand
from django.utils import timezone

from api.engine.models import Reservation


class Command(BaseCommand):
    help = 'Collect the expired reservations quota'

    def handle(self, *args, **kwargs):
        self.stdout.write('Looking for expired reservations...')
        expired_reservations = Reservation.objects.update_expired_reservations()
        self.stdout.write(f'Done, found {expired_reservations} reservations')
