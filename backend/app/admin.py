from django.contrib import admin

from .models import Datasource, Campaign, DayStats, Gaz
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class GazResource(resources.ModelResource):

    class Meta:
        model = Gaz

# вывод данных на странице
class GazAdmin(ImportExportModelAdmin):
    resource_classes = [GazResource]

admin.site.register(Datasource)
admin.site.register(Campaign)
admin.site.register(DayStats)
admin.site.register(Gaz, GazAdmin)