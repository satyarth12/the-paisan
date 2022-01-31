from django.urls import path, include
from .views import RecommendationCreateView, RecommendationListView
from django.db import router
from rest_framework import routers

app_name = "Recommendation"

router = routers.DefaultRouter()
router.register(r'recommendation', RecommendationListView, basename='recommendation')

urlpatterns = [
     path('recommendation/create/', RecommendationCreateView.as_view(),
          name='recommendations-create'),
     path('', include(router.urls))
     # path('recommendations/received', RecommendationListView.as_view(),
     #      name='recommendations'),
     #  path('recommendations/received', RecommendationListView.as_view(),
     #      name='recommendations'),
]         
