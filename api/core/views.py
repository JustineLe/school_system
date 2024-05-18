from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction

import logging

from core.models import (
    School, 
    Course, 
    Administrator, 
    Student, 
    Teacher
)
from core.serializers import (
    SchoolSerializer, 
    CourseSerializer, 
    AdminSerializer, 
    StudentSerializer, 
    TeacherSerializer,
    SchoolStatSerializer
)

logger = logging.getLogger(__name__)


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class AdminViewSet(viewsets.ModelViewSet):
    queryset = Administrator.objects.all()
    serializer_class = AdminSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class SchoolStatView(APIView):
    def get(self, request, pk):
        school = get_object_or_404(School, pk=pk)

        courses_count = Course.objects.filter(school=pk).count()
        admins_count = Administrator.objects.filter(school=pk).count()
        teachers_count = Teacher.objects.filter(school=pk).count()
        students_count = Student.objects.filter(school=pk).count()

        serializer = SchoolStatSerializer({
            'id': school.id,
            'courses': courses_count,
            'admins': admins_count,
            'teachers': teachers_count,
            'students': students_count
        })

        return Response(serializer.data)


class ClassMovementView(APIView):
    def post(self, request):
        # extract data from request body
        student_id = request.data.get('studentId')
        from_course_id = request.data.get('fromCourseId')
        to_course_id = request.data.get('toCourseId')

        if not student_id:
            return Response({
                "message": "student_id must be required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        transfer_student = get_object_or_404(Student, pk=student_id)

        if from_course_id and to_course_id:
            if from_course_id == to_course_id:
                return Response(
                    {"message": "from_course and to_course are the SAME"},
                    status=status.HTTP_200_OK
                )
            from_course = get_object_or_404(Course, pk=from_course_id)
            to_course = get_object_or_404(Course, pk=to_course_id)

            if transfer_student not in from_course.student.all():
                return Response(
                    {"message": "Could not FOUND `student` in the `from_course`"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if transfer_student in to_course.student.all():
                return Response(
                    {"message": "`student` is already existed in `to_course`"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                with transaction.atomic():
                    from_course.student.remove(transfer_student)
                    to_course.student.add(transfer_student)
                    from_course.save()
                    to_course.save()
            except Exception as e:
                return Response({
                    "message": f"Error move student {student_id} from course {from_course_id} to course {to_course_id}"
                },
                status=status.HTTP_400_BAD_REQUEST)

            return Response(
                {
                    "message": f"Student {student_id} moved from course {from_course_id} to course {to_course_id}."
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Both fromCourseId and toCourseId are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
