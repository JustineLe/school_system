from rest_framework.test import APITestCase
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

        self.transfer_url = reverse("class-movement")

    def test_transfer_missing_student_id(self):
        data = {
            "studentId": 9999,
            "fromCourseId": self.course_1.id,
            "toCourseId": self.course_2.id
        }
        response = self.client.post(self.transfer_url, data, format="json")
        self.assertEqual(response.status_code, 404)

    def test_transfer_missing_from_course_id(self):
        data = {
            "studentId": self.student_1.id,
            "fromCourseId": 9999,
            "toCourseId": self.course_2.id
        }
        response = self.client.post(self.transfer_url, data, format="json")
        self.assertEqual(response.status_code, 404)

    def test_transfer_missing_to_course_id(self):
        data = {
            "studentId": self.student_1.id,
            "fromCourseId": self.course_1.id,
            "toCourseId": 9999
        }
        response = self.client.post(self.transfer_url, data, format="json")
        self.assertEqual(response.status_code, 404)

    def test_transfer_exists_same_course(self):
        data = {
            "studentId": self.student_1.id,
            "fromCourseId": self.course_1.id,
            "toCourseId": self.course_1.id
        }
        response = self.client.post(self.transfer_url, data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_transfer_student_id_not_in_from_course(self):
        data = {
            "studentId": self.student_3.id,
            "fromCourseId": self.course_1.id,
            "toCourseId": self.course_2.id
        }
        response = self.client.post(self.transfer_url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "Could not FOUND `student` in the `from_course`")

    def test_transfer_student_id_in_to_course(self):
        data = {
            "studentId": self.student_2.id,
            "fromCourseId": self.course_1.id,
            "toCourseId": self.course_2.id
        }
        response = self.client.post(self.transfer_url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "`student` is already existed in `to_course`")

    def test_transfer_student_success(self):
        data = {
            "studentId": self.student_1.id,
            "fromCourseId": self.course_1.id,
            "toCourseId": self.course_2.id
        }
        response = self.client.post(self.transfer_url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.course_1.student.count() + 1, self.course_2.student.count() - 1)
