from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.serializers import DateField

from . import models


# Create your tests here.
class TestDayStats(APITestCase):
    client = APIClient()
    url = reverse('api:day-stats-list')

    def test_not_allowed_methods(self):
        invalid_methods = [
            'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE'
        ]

        for method in invalid_methods:
            response = self.client.request(method=method, url=self.url)

            self.assertEqual(
                response.status_code,
                status.HTTP_404_NOT_FOUND
            )

    def test_no_filters(self):
        response = self.client.get(
            self.url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {
                'end_date': ['This field is required.'],
                'start_date': ['This field is required.']
            }
        )

    def test_with_filters(self):
        newer_date = timezone.now().date()
        older_date = newer_date - timedelta(days=1)

        d1 = models.Datasource.objects.create(name='d1')
        d2 = models.Datasource.objects.create(name='d2')

        c1 = models.Campaign.objects.create(name='c1')
        c2 = models.Campaign.objects.create(name='c2')

        models.DayStats.objects.create(date=older_date, datasource=d1, campaign=c1, clicks=111, impressions=222)
        s2 = models.DayStats.objects.create(date=newer_date, datasource=d1, campaign=c1, clicks=333, impressions=444)
        s3 = models.DayStats.objects.create(date=newer_date, datasource=d2, campaign=c2, clicks=555, impressions=666)

        response = self.client.get(
            self.url,
            {
                'start_date': newer_date.strftime('%Y-%m-%d'),
                'end_date': (newer_date + timedelta(days=1)).strftime('%Y-%m-%d')
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            [
                {
                    'id': s2.id,
                    'date': DateField().to_representation(s2.date),
                    'datasource': {
                        'id': d1.id,
                        'name': d1.name
                    },
                    'campaign': {
                        'id': c1.id,
                        'name': c1.name
                    },
                    'clicks': 333,
                    'impressions': 444
                },
                {
                    'id': s3.id,
                    'date': DateField().to_representation(s3.date),
                    'datasource': {
                        'id': d2.id,
                        'name': d2.name
                    },
                    'campaign': {
                        'id': c2.id,
                        'name': c2.name
                    },
                    'clicks': 555,
                    'impressions': 666
                }
            ]
        )
