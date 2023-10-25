"""
URL configuration for supermarket_project project.

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

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from supermarket_app.views import CategoryViewSet, ProductViewSet, ItemsViewSet, ShopcardViewSet, CustomerViewSet
from supermarket_app.views import PurchaseHistoryView, TotalPurchaseView, MarketTotalProductsView, ExpiredProductsView, BestSellingProductView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'items', ItemsViewSet)
router.register(r'shopcards', ShopcardViewSet)
router.register(r'customers', CustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('purchase-history/<int:customer_id>/', PurchaseHistoryView.as_view(), name='purchase-history'),
    path('total-purchase/<int:customer_id>/', TotalPurchaseView.as_view(), name='total-purchase'),
    path('market-total-products/', MarketTotalProductsView.as_view(), name='market-total-products'),
    path('expired-products/', ExpiredProductsView.as_view(), name='expired-products'),
    path('best-selling-product/', BestSellingProductView.as_view(), name='best-selling-product'),
]
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Supermarket API",
        default_version='v1',
        description="API for a supermarket application",
        terms_of_service="https://www.supermarketapp.com/terms/",
        contact=openapi.Contact(email="contact@supermarketapp.com"),
        license=openapi.License(name="Supermarket License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('supermarket_app.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
