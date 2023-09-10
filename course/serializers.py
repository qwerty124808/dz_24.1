from rest_framework import serializers
from course.models import Course, Lesson, Payment, Subscription
from course.validators import VideoURLValidator, IsURLValidator
from users.models import User


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__' 
        validators = [
            VideoURLValidator(field_name='url'),
            IsURLValidator(),
        ]

class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        # Если у текущего курса есть подписка с текущем пользователем:
        if obj.subscriptions.filter(user=self.context['request'].user).exists():
            return True

        return False


    class Meta:
        model = Course
        fields = ['id', 'name', 'photo', 'description', 'url', 'lessons','lesson_count', 'user', 'is_subscribed']

        validators = [
            VideoURLValidator(field_name='url'),
            IsURLValidator(),
        ]

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериалайзер"""

    class Meta:
        model = Subscription
        fields = "__all__"