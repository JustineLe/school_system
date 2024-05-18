from django.db import models

from .teacher import Teacher
from .student import Student
from .school import School


class Course(models.Model):
    class Meta:
        unique_together = ('name', 'school')

    name = models.CharField(max_length=128, blank=False, null=False)
    location = models.CharField(max_length=128, blank=False, null=False)
    teacher = models.ForeignKey(to=Teacher, on_delete=models.SET_NULL, null=True, related_name="course_teacher")
    student = models.ManyToManyField(to=Student, blank=True, related_name="course_student")
    school = models.ForeignKey(to=School, on_delete=models.CASCADE, null=False, related_name="school_course", default="")

    def __str__(self):
        return self.name
