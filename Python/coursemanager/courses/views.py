from django.http import HttpResponse

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from .models import Course, Enrollment, Student
from .serializers import CourseSerializer, EnrollmentSerializer, StudentSerializer


def hello_view(request):
	return HttpResponse('Course Management API is running')


class CourseViewSet(viewsets.ModelViewSet):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer

	@action(detail=True, methods=['get'])
	def students(self, request, pk=None):
		course = self.get_object()
		students = Student.objects.filter(enrollments__course=course).distinct()
		serializer = StudentSerializer(students, many=True)
		return Response(serializer.data)


class StudentViewSet(viewsets.ModelViewSet):
	queryset = Student.objects.all()
	serializer_class = StudentSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
	queryset = Enrollment.objects.all()
	serializer_class = EnrollmentSerializer
