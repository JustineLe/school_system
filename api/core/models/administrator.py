from django.db import models

from .school import School


class Administrator(models.Model):
  name = models.CharField(max_length=128, blank=False, null=False)
  school = models.ForeignKey(to=School, on_delete=models.CASCADE, null=False, default="", blank=True, related_name="school_administrator")

  def __str__(self):
        return self.name
