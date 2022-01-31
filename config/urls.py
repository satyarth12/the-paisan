"""bingeman_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

# from api import views
# import oauth2_providers


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Bingeman",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="satyarthdev@protonmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('', include(router.urls)),
    path('', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('api-auth/', include('rest_framework.urls',
         namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('', include('profiling.urls')),
    path('', include('movie_tv.urls')),
    path('', include('connections.urls')),
    path('', include('rating_review.urls')),
    path('', include('recommendation.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),


]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += [
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    ]
