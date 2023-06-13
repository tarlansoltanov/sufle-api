"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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


urlpatterns = [
    path("admin/", admin.site.urls),
]


# Project App URLs
from rest_framework import routers
from server.apps.category.views import CategoryViewSet
from server.apps.product.views import ProductViewSet
from server.apps.announcement.views import BannerViewSet
from server.apps.shop.views import ShopViewSet
from server.apps.contact.views import ContactViewSet
from server.apps.gallery.views import GalleryViewSet

router = routers.DefaultRouter()
router.register(r"category", CategoryViewSet, basename="category")
router.register(r"product", ProductViewSet, basename="product")
router.register(r"banner", BannerViewSet, basename="banner")
router.register(r"shop", ShopViewSet, basename="shop")
router.register(r"contact", ContactViewSet, basename="contact")
router.register(r"gallery", GalleryViewSet, basename="gallery")

urlpatterns += [
    path("api/", include(router.urls)),
    path("api/auth/", include("server.apps.user.urls")),
]


# DRF YASG (Yet Another Swagger Generator)
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="Sufle API",
        default_version="v1",
        description="API for Sufle Project",
    ),
    public=True,
)

urlpatterns += [
    path(
        "api/redoc", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path(
        "api/swagger",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger",
    ),
]


# Health check
urlpatterns += [
    path("health/", include("health_check.urls")),
]


# Django Debug Toolbar
if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
