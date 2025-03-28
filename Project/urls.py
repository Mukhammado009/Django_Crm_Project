from django.contrib import admin
from django.urls import path
from app.views import UserAPIView, GetMe, ClientAPIView, TaskAPIView
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

...

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
   
    path('admin/', admin.site.urls),
    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   
    path('api/users/', UserAPIView.as_view()),
    path('api/users/<int:pk>/', UserAPIView.as_view()),
    path('api/get_me/', GetMe.as_view()),

   
    path('api/clients/', ClientAPIView.as_view()),
    path('api/clients/<int:pk>/', ClientAPIView.as_view()),

 
    path('api/tasks/', TaskAPIView.as_view()),
    path('api/tasks/<int:pk>/', TaskAPIView.as_view()),
]