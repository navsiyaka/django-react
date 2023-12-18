from dataclasses import dataclass
from datetime import datetime
import re
import codecs
import io

from django.core.management.base import BaseCommand
from app import models


@dataclass
class Item:
    subsidiary: str
    subsoil_user: str
    territory_type: str
    cost_item: str
    geographical_segments: str
    licensed_area: str
    data_type: str
    display: str
    value: int


class Command(BaseCommand):
    """Django command that waits for database to be available"""

    def add_arguments(self, parser):
        parser.add_argument('input_csv_path', nargs=1, type=str)

    def handle(self, *args, **options):
        """Handle the command"""
        input_csv_path = options['input_csv_path'][0]
        with io.open(input_csv_path, encoding='utf-8') as input_csv_file:
            input_csv_text = input_csv_file.read()
            print(input_csv_text)

        matches = re.findall(r'(.*);(.*);(.*);(.*);(.*);(.*);(.*);(.*);(\d+)', input_csv_text)

        items = []
        for match in matches:
            subsidiary = match[0]
            subsoil_user = match[1]
            territory_type = match[2]
            cost_item = match[3]
            geographical_segments = match[4]
            licensed_area = match[5]
            data_type = match[6]
            display = match[7]
            value = int(match[8])

            items.append(Item(subsidiary, subsoil_user, territory_type, cost_item, geographical_segments, licensed_area, data_type, display, value))

        print(f'Found {len(items)} items')

        models.Gaz.objects.bulk_create(
            (
                models.Gaz(
                    subsidiary=item.subsidiary,
                    subsoil_user = item.subsoil_user,
                    territory_type = item.territory_type,
                    cost_item = item.cost_item,
                    geographical_segments = item.geographical_segments,
                    licensed_area = item.licensed_area,
                    data_type = item.data_type,
                    display = item.display,
                    value = item.value
                )
                for item in items
            )
        )

        print(f'Created {len(items)} day stats')


if __name__ == '__main__':
    import django
    from django.conf import settings
    from project import settings as project_settings

    settings.configure(**project_settings.__dict__)
    django.setup()

    Command().handle()
