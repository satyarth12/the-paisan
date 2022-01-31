from . import views
from rest_framework import routers
from django.urls import path, include
# from rest_framework.authtoken.views import obtain_auth_token


router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user'),
router.register(r'referral', views.ReffView, basename='referral')

urlpatterns = [

    path('', include(router.urls)),
    path('register/', views.RegisterUserViewSet.as_view()),
    path('auth/', views.customAuthToken.as_view()),
    path('socialauth/', include('rest_framework_social_oauth2.urls')),

    # path('user/useractivity/create/',
    #      views.UserActivityCreateView.as_view(), name='useractivity-create'),
]
