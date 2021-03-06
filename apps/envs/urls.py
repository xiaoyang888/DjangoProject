from django.urls import path, re_path

from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views

# 定义路由对象
router = DefaultRouter()
router.register(r'envs', views.EnvsViewSet)

urlpatterns = [
]
urlpatterns += router.urls
