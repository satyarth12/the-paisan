from . import views
from rest_framework import routers
from django.urls import path, include

from . import views


router = routers.DefaultRouter()
router.register(r'movie', views.MovieViewSet, basename='movie'),
router.register(r'tv', views.TVViewSet, basename='tv')

urlpatterns = [

    path('', include(router.urls)),

]
