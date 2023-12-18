from dataclasses import dataclass
from datetime import datetime
import re

from django.core.management.base import BaseCommand
from app import models


@dataclass
class Item:
    date: datetime
    datasource: str
    campaign: str
    clicks: int
    impressions: int


class Command(BaseCommand):
    """Django command that waits for database to be available"""

    def add_arguments(self, parser):
        parser.add_argument('input_csv_path', nargs=1, type=str)

    def handle(self, *args, **options):
        """Handle the command"""
        input_csv_path = options['input_csv_path'][0]
        with open(input_csv_path) as input_csv_file:
            input_csv_text = input_csv_file.read()

        matches = re.findall(r'(\d+\.\d+\.\d+),(.*),(.*),(\d+),(\d+)', input_csv_text)

        items = []
        for match in matches:
            date = datetime.strptime(match[0], '%d.%m.%Y')
            datasource = match[1]
            campaign = match[2]
            clicks = int(match[3])
            impressions = int(match[4])

            items.append(Item(date, datasource, campaign, clicks, impressions))

        print(f'Found {len(items)} items')

        new_datasources = set(i.datasource for i in items)
        new_campaigns = set(i.campaign for i in items)

        print(f'Found {len(new_datasources)} datasources')
        print(f'Found {len(new_campaigns)} campaigns')

        models.Datasource.objects.bulk_create(
            (models.Datasource(name=name) for name in new_datasources),
            ignore_conflicts=True
        )

        print(f'Created datasources')

        models.Campaign.objects.bulk_create(
            (models.Campaign(name=name) for name in new_campaigns),
            ignore_conflicts=True
        )

        print(f'Created campaigns')

        datasources_by_name = {m.name: m for m in models.Datasource.objects.all()}
        campaigns_by_name = {m.name: m for m in models.Campaign.objects.all()}

        models.DayStats.objects.bulk_create(
            (
                models.DayStats(
                    date=item.date,
                    datasource=datasources_by_name[item.datasource],
                    campaign=campaigns_by_name[item.campaign],
                    clicks=item.clicks,
                    impressions=item.impressions
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
