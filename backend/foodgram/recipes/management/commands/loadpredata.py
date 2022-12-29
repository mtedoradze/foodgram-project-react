import csv
import os

from django.conf import settings
from django.core.management import BaseCommand
from recipes.models import Ingredient, Tag

MODEL_FILE = {
    Ingredient: "ingredients.csv",
    Tag: "tags.csv"
}


class Command(BaseCommand):
    help = "Загружаем данные из csv-файла в базу данных."

    def handle(self, *args, **kwargs):
        for model, file in MODEL_FILE.items():
            with open(
                os.path.join(settings.BASE_DIR, 'static/data/', file),
                'r', encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(
                    model(**data) for data in reader
                )

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))
