from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import hello_view, CourseViewSet, StudentViewSet, EnrollmentViewSet

# Initialize DefaultRouter
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    path('hello/', hello_view, name='hello'),
    path('', include(router.urls)),
]
