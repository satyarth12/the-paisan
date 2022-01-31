from django.urls import path, include
from rest_framework import routers

from profiling.views.lists import (
    FavourtelistView, WatchlistView, WatchedlistView)
from profiling.views.profile_views import ProfileViewset
from profiling.views.interest import InterestView
from profiling.views.report_views import ReportCreateView
from profiling.views.block_views import BlockCreateView

app_name = 'profiling'

router = routers.DefaultRouter()
router.register(r'profile', ProfileViewset, basename='profile')
router.register(r'favoritelist', FavourtelistView, basename='favoritelist')
router.register(r'watchlist', WatchlistView, basename='watchlist')
router.register(r'watchedlist', WatchedlistView, basename='watchedlist')
router.register(r'interest', InterestView, basename='interest')


urlpatterns = [

    path('', include(router.urls)),
    path('report/', ReportCreateView.as_view()),  # Done
    path('block/', BlockCreateView.as_view()),  # Done

]
