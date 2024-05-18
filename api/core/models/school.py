from django.db import models


class School(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    address = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.name
