from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import routers

from core import views as core_views


schema_view = get_schema_view(
   openapi.Info(
      title="School API",
      default_version='v1',
      description="School system",
      terms_of_service="",
      contact=openapi.Contact(email=""),
      license=openapi.License(name=""),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

api_router = routers.DefaultRouter(trailing_slash=False)

# school url
api_router.register(r"schools", core_views.SchoolViewSet, basename='school')

# course url
api_router.register(r"course", core_views.CourseViewSet, basename='course')

# admin url
api_router.register(r"administrator", core_views.AdminViewSet, basename='administrator')

# student url
api_router.register(r"student", core_views.StudentViewSet, basename='student')

# teacher url
api_router.register(r"teacher", core_views.TeacherViewSet, basename='teacher')


urlpatterns =  [
    path('admin/', admin.site.urls),
    path('api/', include(api_router.urls)),
    path('api/school/<int:pk>/stat', core_views.SchoolStatView.as_view(), name='school-stat'),
    path('api/transfer', core_views.ClassMovementView.as_view(), name='class-movement'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]