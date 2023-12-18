from rest_framework import viewsets, mixins
from rest_framework import permissions
from django_filters import rest_framework as filters

from . import models
from . import serializers

"""
django-filter library:
https://django-filter.readthedocs.io/en/main/ref/filters.html

options for choices criteria in json:

lookup_choices = [
    ('exact', 'Equals'),
    ('gt', 'Greater than'),
    ('lt', 'Less than'),
    ('in', in this range, exclude right value),
    ('range', in this range, include right value),
]

filter types: 
CharFilter, UUIDFilter, ChoiceFilter
(This filter matches values in its choices argument),
DateFilter, NumberFilter, BooleanFilter
"""


class ProductFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='date', lookup_expr='lte')
    min_clicks = filters.NumberFilter(field_name='clicks', lookup_expr='exact')
    # max_clicks = filters.NumberFilter(field_name='clicks', lookup_expr='lte')


"""
create views with all methods

"""


class DayStatsViewset(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = models.DayStats.objects.select_related('datasource', 'campaign')
    serializer_class = serializers.DayStatsSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter

    # @action(methods=['get'], detail=True)
    # def datasources(self, request, pk=None):
    #     datasource = models.Datasource.objects.get(pk=pk)
    #     return Response({'datasource': datasource.name})


class GazViewset(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = models.Gaz.objects.all()
    serializer_class = serializers.GazSerializer
