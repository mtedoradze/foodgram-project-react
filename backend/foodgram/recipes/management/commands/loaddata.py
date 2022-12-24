import csv
import os

from django.conf import settings
from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Загружаем данные из csv-файла в базу данных."

    def handle(self, *args, **kwargs):
        with open(
            os.path.join(settings.BASE_DIR, 'static/data/ingredients.csv'),
            'r', encoding='utf-8'
        ) as csv_file:
            reader = csv.DictReader(csv_file)
            Ingredient.objects.bulk_create(
                Ingredient(**data) for data in reader
            )

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))
