from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .authentication import UUIDJWTAuthentication

schema_view = get_schema_view(
   openapi.Info(
      title="FilmFusion API",
      default_version='v1',
      description="API documentation for the User and Post Services",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   authentication_classes=[UUIDJWTAuthentication], 
)
