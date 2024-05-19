from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.models import School, Teacher, Student, Administrator, Course


class ExtensionAPITestCase(APITestCase):
    def setUp(self):
        self.school = School.objects.create(name="Test School")

        self.admin = Administrator.objects.create(name="Test Admin", school=self.school)

        self.teacher_1 = Teacher.objects.create(name="Teacher 1", school=self.school)
        self.teacher_2 = Teacher.objects.create(name="Teacher 2", school=self.school)

        self.student_1 = Student.objects.create(name="Student 1", school=self.school)
        self.student_2 = Student.objects.create(name="Student 2", school=self.school)
        self.student_3 = Student.objects.create(name="Student 3", school=self.school)

        self.course_1 = Course.objects.create(name="Python", teacher=self.teacher_1, school=self.school)
        self.course_1.student.add(self.student_1, self.student_2)
        self.course_2 = Course.objects.create(name="Django", teacher=self.teacher_2, school=self.school)
        self.course_2.student.add(self.student_2, self.student_3)

    def test_get_school_stats_successfully(self):
        school_stats_url = reverse("school-stat", kwargs={'pk': self.school.pk})
        response = self.client.get(school_stats_url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["courses"], 2)
        self.assertEqual(response.data["admins"], 1)
        self.assertEqual(response.data["teachers"], 2)
        self.assertEqual(response.data["students"], 3)

    def test_missing_school_stats(self):
        school_stats_url = reverse("school-stat", kwargs={'pk': 9999})
        response = self.client.get(school_stats_url, format="json")
        self.assertEqual(response.status_code, 404)
