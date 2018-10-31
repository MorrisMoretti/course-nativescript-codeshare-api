from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from djangocrud.api import views
from django.conf import settings
from django.conf.urls.static import static
from djangocrud.api.views import CustomObtainAuthToken

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'movies', views.MovieViewSet)
router.register(r'reviews', views.ReviewViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^auth/', CustomObtainAuthToken.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
