from django.urls import path, include, re_path
from django.shortcuts import redirect
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

schema_view = get_schema_view(
    openapi.Info(
        title="Nanny's Pet API",
        default_version='v1',
        description="API para o Nanny's Pet",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@nannys.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],  # ← isso desativa a exigência de token no Swagger
)


# Redireciona a raiz para o Swagger UI
def redirect_to_swagger(request):
    return redirect('schema-swagger-ui', permanent=False)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Redireciona a raiz para o Swagger UI
    path('', redirect_to_swagger),

    path('api/', include('nanny_pets_app.urls')),

    # Swagger e Redoc
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
