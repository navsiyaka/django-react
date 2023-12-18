from django.db import models


class NameModel(models.Model):
    name = models.CharField(max_length=80, unique=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return f'{self.__class__.__name__} {self.name!r} (id={self.id!r})'


class Datasource(NameModel):
    pass


class Campaign(NameModel):
    pass


class DayStats(models.Model):
    date = models.DateField()
    datasource = models.ForeignKey(Datasource, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    clicks = models.IntegerField()
    impressions = models.IntegerField()

    class Meta:
        ordering = ['date', 'datasource', 'campaign']
        # unique_together = ['date', 'datasource', 'campaign']

    def __str__(self):
        return f'{self.__class__.__name__} date={self.date!s}'


class Gaz(models.Model):
    subsidiary = models.CharField(max_length=80, null=True,
                                  verbose_name='Дочернее общество')
    subsoil_user = models.CharField(max_length=80, null=True,
                                    verbose_name='Недропользователь')
    territory_type = models.CharField(max_length=80, null=True,
                                      verbose_name='Тип территории')
    cost_item = models.CharField(max_length=80, null=True,
                                 verbose_name='Статья затрат')
    geographical_segments = models.CharField(max_length=80, null=True,
                                             verbose_name='Географические сегменты')
    licensed_area = models.CharField(max_length=80, null=True,
                                     verbose_name='Лицензионный участок')
    data_type = models.CharField(max_length=80, null=True,
                                 verbose_name='Тип данных')
    display = models.CharField(max_length=80, null=True,
                               verbose_name='Показатель')
    value = models.IntegerField(null=True,
                                verbose_name='Значение')

    # class Meta:
    #     unique_together = ['subsidiary', 'subsoil_user', 'territory_type',
    #                        'cost_item', 'geographical_segments',
    #                        'licensed_area',
    #                        'data_type', 'display', 'value']

    def __str__(self):
        return f'{self.__class__.__name__} (id={self.id!r})'
