from rest_framework import serializers
from course.models import Course, Lesson, Payment

class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__' 

class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ['id', 'name', 'photo', 'description', 'lesson_count', 'user']

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'