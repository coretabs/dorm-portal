from django.core.management.base import BaseCommand
from django.utils import timezone

from features.steps import factory


class Command(BaseCommand):
    help = 'Seed the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding the database...')
        factory.create_alfam_dovec_with_4_rooms_localized_en_tr(self)
        self.stdout.write('Done !')
