"""URL routes for the courses app."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, EnrollmentViewSet, StudentViewSet, hello_view

router = DefaultRouter()
router.register('courses', CourseViewSet)
router.register('students', StudentViewSet)
router.register('enrollments', EnrollmentViewSet)

urlpatterns = [
    path('hello/', hello_view),
    path('', include(router.urls)),
]