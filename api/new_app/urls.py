from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from core import views as core_views

api_router = routers.DefaultRouter(trailing_slash=False)

# school url
api_router.register(r"schools", core_views.SchoolViewSet, basename='school-list')
api_router.register(r"schools/<int:pk>", core_views.SchoolViewSet, basename='school-detail')

# course url
api_router.register(r"course", core_views.CourseViewSet, basename='course-list')
api_router.register(r"course/<int:pk>", core_views.CourseViewSet, basename='course-detail')

# admin url
api_router.register(r"administrator", core_views.AdminViewSet, basename='administrator-list')
api_router.register(r"administrator/<int:pk>", core_views.AdminViewSet, basename='administrator-detail')

# student url
api_router.register(r"student", core_views.StudentViewSet, basename='student-list')
api_router.register(r"student/<int:pk>", core_views.StudentViewSet, basename='student-detail')

# teacher url
api_router.register(r"teacher", core_views.TeacherViewSet, basename='teacher-list')
api_router.register(r"teacher/<int:pk>", core_views.TeacherViewSet, basename='teacher-detail')


urlpatterns =  [
    path('admin/', admin.site.urls),
    path('api/', include(api_router.urls)),
    path('api/school/<int:pk>/stat', core_views.SchoolStatView.as_view(), name='school-stat'),
    path('api/transfer', core_views.ClassMovementView.as_view(), name='class-movement')
]