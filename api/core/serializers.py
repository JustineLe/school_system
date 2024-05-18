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


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["id", "name", "school"]


class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    student = StudentSerializer(many=True)

    class Meta:
        model = Course
        fields = ["id", "name", "location", "school", "teacher", "student"]

    def validate(self, attrs):
        """
            Validate if student and teacher are in the same school
        """
        teacher_name = attrs.get('teacher')['name']
        student_ids = attrs.get('student')

        teacher_data = Teacher.objects.filter(name=teacher_name).first()

        if not teacher_data:
            raise serializers.ValidationError(f"Not found the teacher with ID {teacher_name}")

        student_count = Student.objects.filter(pk__in=student_ids).count()

        if student_count != len(student_ids):
            raise serializers.ValidationError("One of the input student is invalid!")

        student_school_data = Student.objects.filter(pk__in=student_ids).values_list('school', flat=True)
        
        if set(student_school_data) != teacher_data.school:
            raise serializers.ValidationError("Input teacher and student are not in the same school")
    
    def create(self, validated_data):
        new_course = Course.objects.create(
            
        )


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
