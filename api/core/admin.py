from django.apps import apps
from django.contrib import admin

from core.models import Course

models = apps.get_models()


class CourseStudentInline(admin.TabularInline):
    model = Course.student.through


class CourseAdmin(admin.ModelAdmin):
    inlines = [CourseStudentInline]


for model in models:
    try:
        if model.__name__ == 'Course':
            admin.site.register(model, CourseAdmin)
        else:
            admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
