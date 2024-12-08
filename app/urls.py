from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from app.core.views import CompanyViewSet, DocumentViewSet, SignerViewSet

schema_view = get_schema_view(
    openapi.Info(
        title='ZapSign API',
        default_version='v1',
        description='API para gerenciamento de empresas, documentos e signatários usando DRF.',
        terms_of_service='https://www.teste.com/policies/terms/',
        contact=openapi.Contact(email='suporte@teste.com'),
        license=openapi.License(name='None'),
    ),
    public=True,
    permission_classes=(AllowAny,),
    authentication_classes=[],
)

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'signers', SignerViewSet, basename='signer')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(
        r'^$',
        RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False),
    ),
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
