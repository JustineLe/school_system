from django.db import models

from .school import School


class Student(models.Model):
    class Meta:
        unique_together = ('name', 'school')

    name = models.CharField(max_length=128, blank=False, null=False)
    school = models.ForeignKey(to=School, on_delete=models.CASCADE, null=False, default="", related_name="school_student")

    def __str__(self):
        return self.name
