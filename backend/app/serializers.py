from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from drf_writable_nested import WritableNestedModelSerializer
from . import models


class DatasourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Datasource
        fields = '__all__'
        # extra_kwargs = {
        #     'name': {'validators': []},
        # }


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Campaign
        fields = '__all__'
        # extra_kwargs = {
        #     'name': {'validators': []},
        # }


class DayStatsSerializer(WritableNestedModelSerializer,
                         serializers.ModelSerializer):
    datasource = DatasourceSerializer(read_only=True)
    campaign = CampaignSerializer(read_only=True)

    class Meta:
        model = models.DayStats
        fields = (
            'id', 'date', 'clicks', 'impressions', 'datasource', 'campaign')

class GazSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Gaz
        fields = '__all__'