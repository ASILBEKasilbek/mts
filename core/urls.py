# uzmat/urls.py
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from services import views as service_views
from accounts import views as account_views
from orders import views as order_views
from admin_panel import views as admin_views


schema_view = get_schema_view(
    openapi.Info(
        title="UZMAT.uz API",
        default_version="v1",
        description="API for UZMAT.uz - Online service ordering and delivery platform",
        terms_of_service="https://u-mts.uz/terms/",
        contact=openapi.Contact(email="support@uzmat.uz"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),

    # Authentication
    path("auth/register/", account_views.RegisterView.as_view(), name="register"),
    path("auth/login/", account_views.LoginView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="refresh"),

    # Products
    path("api/products/", service_views.ProductList.as_view(), name="products"),
    path("api/products/paginated/", service_views.PaginatedProductList.as_view(), name="products_paginated"),
    path("api/products/<int:id>/increment-view/", service_views.ProductIncrementView.as_view(), name="increment_view"),
    path("api/products/<int:id>/toggle-like/", service_views.ProductToggleLike.as_view(), name="toggle_like"),
    path("api/products/<slug:slug>/", service_views.ProductDetail.as_view(), name="product_detail"),
    path("edit/<int:id>/", service_views.EditProduct.as_view(), name="edit_product"),

    # Equipment
    path("api/equipment/", service_views.EquipmentList.as_view(), name="equipment"),
    path("api/equipment/paginated/", service_views.PaginatedEquipmentList.as_view(), name="equipment_paginated"),
    path("api/equipment/<int:id>/increment-view/", service_views.EquipmentIncrementView.as_view(), name="equipment_increment"),

    # News
    path("api/news/", service_views.NewsList.as_view(), name="news"),
    path("api/news/paginated/", service_views.PaginatedNewsList.as_view(), name="news_paginated"),
    path("api/news/<int:id>/", service_views.NewsDetail.as_view(), name="news_detail"),
    path("api/news/<int:id>/increment-view/", service_views.NewsIncrementView.as_view(), name="news_increment"),

    # Hot Offers
    path("api/hot-offers/", service_views.HotOfferList.as_view(), name="hot_offers"),
    path("api/hot-offers/paginated/", service_views.PaginatedHotOfferList.as_view(), name="hot_offers_paginated"),
    path("api/hot-offers/product/<slug:slug>/", service_views.HotOfferDetail.as_view(), name="hot_offer_detail"),

    # Ads
    path("api/ads/<slug:slug>/", service_views.AdDetail.as_view(), name="ad_detail"),

    # Accounts & Companies
    path("users/<int:id>/", account_views.UserDetail.as_view(), name="user_detail"),
    path("profile/my-products/statistic/<int:id>/", account_views.MyProductStats.as_view(), name="my_product_stats"),
    path("api/profile/my-applications/statistic/<int:id>/", account_views.MyApplicationStats.as_view(), name="my_application_stats"),
    path("api/about-company/<slug:slug>/", account_views.CompanyDetail.as_view(), name="company_detail"),
    path("api/companies/", account_views.CompanyList.as_view(), name="companies"),

    # Orders & Payments
    path("api/orders/create/", order_views.CreateOrder.as_view(), name="create_order"),
    path("api/orders/<int:id>/status/", order_views.OrderStatus.as_view(), name="order_status"),
    path("api/payments/process/", order_views.ProcessPayment.as_view(), name="process_payment"),

    # Admin Panel APIs
    path("admin/users/", admin_views.AdminUserList.as_view(), name="admin_users"),
    path("admin/services/<int:id>/approve/", admin_views.ApproveService.as_view(), name="approve_service"),

    # API Docs
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
