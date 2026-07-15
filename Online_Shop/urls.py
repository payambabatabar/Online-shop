from django.contrib import admin
from django.urls import path,include
from shop.views import ProductViewset
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title = "Product API",
        default_version = 'v1',
        description = "Product API",
    ),
    public=True,
    permission_classes = [permissions.AllowAny],

)

router = DefaultRouter()
router.register('products', ProductViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('shop.urls')),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('token/verify', TokenVerifyView.as_view()),
    path('api/swagger/', schema_view.with_ui('swagger'), name='schema_swagger')
]
