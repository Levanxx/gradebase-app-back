# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

# Swagger/OpenAPI
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# JWT (views)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    # TokenVerifyView,  # opcional
)

urlpatterns = [
    # Redirección raíz → Swagger
    path("", RedirectView.as_view(url="/api/docs/swagger/", permanent=False)),

    # Admin
    path("admin/", admin.site.urls),

    # API del app (router + actions)
    path("api/", include("core.urls")),

    # JWT (autenticación)
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # OpenAPI schema + docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
