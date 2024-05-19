from rest_framework import serializers

from core.models import School, Course, Administrator, Student, Teacher


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = ["id", "name", "school"]


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "name", "school"]

    def validate(self, attrs):
        try:
            course_belong_to_student = self.instance.course_student.all().first()
        except AttributeError:
            course_belong_to_student = None

        if course_belong_to_student:
            course_school_id = course_belong_to_student.school.id
            course_school_name = course_belong_to_student.school.name
        if course_belong_to_student and (course_school_id != attrs['school']):
            raise serializers.ValidationError(
                f"Student {self.instance.name} is in a course belong to school {course_school_name}"
                )

        return attrs


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["id", "name", "school"]

    def validate(self, attrs):
        try:
            course_belong_to_teacher = self.instance.course_teacher.all().first()
        except AttributeError:
            course_belong_to_teacher = None

        if course_belong_to_teacher:
            course_school_id = course_belong_to_teacher.school.id
            course_school_name = course_belong_to_teacher.school.name
        if course_belong_to_teacher and (course_school_id != attrs['school']):
            raise serializers.ValidationError(
                f"Teacher {self.instance.name} is in a course belong to school {course_school_name}"
                )

        return attrs


class CourseSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(many=True, queryset=Student.objects.all())

    class Meta:
        model = Course
        fields = ["id", "name", "location", "school", "teacher", "student"]

    def validate(self, attrs):
        students = attrs["student"]
        school = attrs["school"]
        teacher = attrs["teacher"]

        if teacher and (teacher.school.id != school.id):
            raise serializers.ValidationError("Teacher's school is not the same")
        for ind, student in enumerate(students):
            if student.school.id != school.id:
                raise serializers.ValidationError(f"index-{ind} student's school is not the same")

        return attrs


class SchoolSerializer(serializers.ModelSerializer):
    school_course = CourseSerializer(many=True, read_only=True)
    school_teacher = TeacherSerializer(many=True, read_only=True)
    school_student = StudentSerializer(many=True, read_only=True)
    school_administrator = AdminSerializer(many=True, read_only=True)

    class Meta:
        model = School
        fields = ["id", "name", "address", "school_course", "school_teacher", "school_student", "school_administrator"]


class SchoolStatSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    courses = serializers.IntegerField(read_only=True)
    admins = serializers.IntegerField(read_only=True)
    teachers = serializers.IntegerField(read_only=True)
    students = serializers.IntegerField(read_only=True)
