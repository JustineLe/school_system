from core.models import School, Teacher, Student, Administrator, Course
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

import json


class ParticipantAPITestCase(APITestCase):
    def setUp(self):
        self.school = School.objects.create(name="Test School", address="Mars")
        self.admin = Administrator.objects.create(name="Test Admin", school=self.school)
        self.teacher = Teacher.objects.create(name="Test Teacher", school=self.school)
        self.student = Student.objects.create(name="Test Student", school=self.school)

        self.second_school = School.objects.create(name="Second School", address="Jupiter")
        self.second_admin = Administrator.objects.create(name="Test Admin 2", school=self.second_school)
        self.second_teacher = Teacher.objects.create(name="Test Teacher 2", school=self.second_school)
        self.second_student = Student.objects.create(name="Test Student 2", school=self.second_school)
        self.second_course = Course.objects.create(
            name="Test Course",
            location="Test Location",
            school=self.second_school,
            # teacher=self.second_teacher,
        )
        # self.second_course.student.add(*[self.second_student])

        self.school_list_url = reverse("school-list")
        self.admin_list_url = reverse("administrator-list")
        self.teacher_list_url = reverse("teacher-list")
        self.student_list_url = reverse("student-list")
        self.course_list_url = reverse("course-list")

        self.school_update_url = reverse("school-detail", kwargs={'pk': self.school.id})
        self.admin_update_url = reverse("administrator-detail", kwargs={'pk': self.admin.id})
        self.teacher_update_url = reverse("teacher-detail", kwargs={'pk': self.teacher.id})
        self.student_update_url = reverse("student-detail", kwargs={'pk': self.student.id})

    def test_create_course(self):
        data = {
            "name": "New Course",
            "location": "New Location",
            "school": self.second_school.id,
            "student": [],
            "teacher": None
        }
        response = self.client.post(self.course_list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(Course.objects.get(id=response.data["id"]).name, "New Course")

    def test_create_course_fail_with_school_id_and_student_school_not_same(self):
        """
        Test if courser's school is same as the student's school
        """
        data = {
            "name": "New Course",
            "location": "New Location",
            "school": self.second_school.id,
            "student": [self.student.id],
            "teacher": None
        }
        response = self.client.post(self.course_list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_course_fail_with_school_id_and_teacher_school_not_same(self):
        """
        Test if course's chool is same as the teacher's school
        """
        data = {
            "name": "New Course",
            "location": "New Location",
            "school": self.second_school.id,
            "student": [],
            "teacher": self.teacher.id
        }
        response = self.client.post(self.course_list_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_school(self):
        data = {
            "name": "New School",
            "address": "Earth",
        }
        response = self.client.post(self.school_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(School.objects.count(), 3)
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

    def test_get_detail_school(self):
        response = self.client.get(self.school_update_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Test School")

    def test_get_detail_school_not_found_school_id(self):
        response = self.client.get(reverse("school-detail", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, 404)

    def test_get_detail_admin(self):
        response = self.client.get(reverse("administrator-detail", kwargs={"pk": self.admin.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Test Admin")

    def test_get_detail_admin_not_found_admin_id(self):
        response = self.client.get(reverse("administrator-detail", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, 404)

    def test_get_detail_teacher(self):
        response = self.client.get(reverse("teacher-detail", kwargs={"pk": self.teacher.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Test Teacher")

    def test_get_detail_teacher_not_found_teacher_id(self):
        response = self.client.get(reverse("teacher-detail", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, 404)

    def test_get_detail_student(self):
        response = self.client.get(reverse("student-detail", kwargs={"pk": self.student.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Test Student")

    def test_get_detail_student_not_found_student_id(self):
        response = self.client.get(reverse("student-detail", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, 404)

    def test_update_school(self):
        new_data = {
            'name': 'Updated School',
            'address': 'Updated Address'
        }
        response = self.client.put(
            self.school_update_url,
            data=json.dumps(new_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.school.id)
        self.assertEqual(response.json()['name'], new_data['name'])
        self.assertEqual(response.json()['address'], new_data['address'])

        self.school.refresh_from_db()
        self.assertEqual(self.school.name, new_data['name'])
        self.assertEqual(self.school.address, new_data['address'])

    def test_update_school_partial(self):
        new_data = {
            'name': 'Partially Updated School'
        }
        response = self.client.patch(
            self.school_update_url,
            data=json.dumps(new_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.school.id)
        self.assertEqual(response.json()['name'], new_data['name'])

        self.school.refresh_from_db()
        self.assertEqual(self.school.name, new_data['name'])

    def test_update_school_invalid_json(self):
        response = self.client.put(
            self.school_update_url,
            data='invalid-json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_update_admin(self):
        new_data = {
            'name': 'Updated Admin',
            'school': self.second_school.id
        }
        response = self.client.put(
            self.admin_update_url,
            data=json.dumps(new_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.admin.id)
        self.assertEqual(response.json()['name'], new_data['name'])

        self.admin.refresh_from_db()
        self.assertEqual(self.admin.name, new_data['name'])

    def test_update_admin_partial(self):
        new_data = {
            'name': 'Partially Updated Admin'
        }
        response = self.client.patch(
            self.admin_update_url,
            data=json.dumps(new_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.admin.id)
        self.assertEqual(response.json()['name'], new_data['name'])

        self.admin.refresh_from_db()
        self.assertEqual(self.admin.name, new_data['name'])

    def test_update_admin_invalid_json(self):
        response = self.client.put(
            self.admin_update_url,
            data='invalid-json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_update_teacher(self):
        new_data = {
            'name': 'Updated Teacher',
            'school': self.second_school.id
        }
        response = self.client.put(
            self.teacher_update_url,
            data=json.dumps(new_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.teacher.id)
        self.assertEqual(response.json()['name'], new_data['name'])

        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.name, new_data['name'])

    def test_update_teacher_partial(self):
        new_data = {
            'name': 'Partially Updated Teacher'
        }
        response = self.client.patch(
            self.teacher_update_url,
            data=json.dumps(new_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.teacher.id)
        self.assertEqual(response.json()['name'], new_data['name'])

        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.name, new_data['name'])

    def test_update_teacher_invalid_json(self):
        response = self.client.put(
            self.teacher_update_url,
            data='invalid-json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_update_teacher_to_school_not_in_course(self):
        new_data = {
            'school': self.school.id
        }
        response = self.client.put(
            reverse('teacher-detail', kwargs={'pk': self.second_teacher.id}),
            data=json.dumps(new_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_update_student(self):
        new_data = {
            'name': 'Updated Student',
            'school': self.second_school.id
        }
        response = self.client.put(
            self.student_update_url,
            data=json.dumps(new_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.student.id)
        self.assertEqual(response.json()['name'], new_data['name'])

        self.student.refresh_from_db()
        self.assertEqual(self.student.name, new_data['name'])

    def test_update_student_partial(self):
        new_data = {
            'name': 'Partially Updated Student'
        }
        response = self.client.patch(
            self.student_update_url,
            data=json.dumps(new_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.student.id)
        self.assertEqual(response.json()['name'], new_data['name'])

        self.student.refresh_from_db()
        self.assertEqual(self.student.name, new_data['name'])

    def test_update_student_invalid_json(self):
        response = self.client.put(
            self.student_update_url,
            data='invalid-json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_update_student_to_school_not_in_course(self):
        new_data = {
            'school': self.school.id
        }
        response = self.client.put(
            reverse('student-detail', kwargs={'pk': self.second_student.id}),
            data=json.dumps(new_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
