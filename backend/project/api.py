from rest_framework import routers
from app import views

#toDo убрать роутер в urls
router = routers.DefaultRouter()

router.register(r'day-stats', views.DayStatsViewset, basename='day-stats')
router.register(r'gaz', views.GazViewset, basename='gaz')