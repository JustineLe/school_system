from core.models import School, Teacher, Student, Administrator, Course
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ParticipantAPITestCase(APITestCase):
    def setUp(self):
        self.school = School.objects.create(name="Test School", address="Mars")
        self.admin = Administrator.objects.create(name="Test Admin", school=self.school)
        self.teacher = Teacher.objects.create(name="Test Teacher", school=self.school)
        self.student = Student.objects.create(name="Test Student", school=self.school)

        self.second_admin = Administrator.objects.create(name="Test Admin 2")
        self.second_teacher = Teacher.objects.create(name="Test Teacher 2")
        self.second_student = Student.objects.create(name="Test Student 2")
        self.course = Course.objects.create(
            name="Test Course",
            location="Test Location",
            teacher=self.second_teacher,
        )
        self.course.student.set([self.second_student])

        self.school_list_url = reverse("school-list-list")
        self.admin_list_url = reverse("administrator-list-list")
        self.teacher_list_url = reverse("teacher-list-list")
        self.student_list_url = reverse("student-list-list")

    def test_create_school(self):
        data = {
            "name": "New School",
            "address": "Earth",
            "school_student": [{"id": self.second_student.id, "name": self.second_student}],
            "school_teacher": [{"id": self.second_teacher.id, "name": self.second_teacher}],
            "school_administrator": [{"id": self.second_admin.id, "name": self.second_admin}],
            "school_course": [{
                "id": self.course.id,
                "name": self.course.name,
                "location": self.course.location,
                "teacher": {
                    "id": self.second_teacher.id,
                    "name": self.second_teacher
                },
                "student": [
                    {
                        "id": self.second_student.id,
                        "name": self.second_student
                    }
                ]
            }]
        }
        response = self.client.post(self.school_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(School.objects.count(), 2)
        self.assertEqual(School.objects.get(id=response.data["id"]).name, "New School")

    def test_create_admin(self):
        data = {"name": "New Admin", "school": self.school.id}
        response = self.client.post(self.admin_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Administrator.objects.count(), 3)
        self.assertEqual(Administrator.objects.get(id=response.data["id"]).name, "New Admin")

    def test_create_teacher(self):
        data = {"name": "New Teacher", "school": self.school.id}
        response = self.client.post(self.teacher_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Teacher.objects.count(), 3)
        self.assertEqual(Teacher.objects.get(id=response.data["id"]).name, "New Teacher")

    def test_create_student(self):
        data = {"name": "New Student", "school": self.school.id}
        response = self.client.post(self.student_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 3)
        self.assertEqual(Student.objects.get(id=response.data["id"]).name, "New Student")

    def test_list_schools(self):
        response = self.client.get(self.school_list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_list_admin(self):
        response = self.client.get(self.admin_list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_list_teachers(self):
        response = self.client.get(self.teacher_list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_list_students(self):
        response = self.client.get(self.student_list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
