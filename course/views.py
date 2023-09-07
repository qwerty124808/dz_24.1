from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from course.models import Course, Lesson, Payment
from course.serializers import CourseSerializer, LessonSerializer, PaymentSerializer 
from rest_framework.permissions import IsAuthenticated, AllowAny
from course.permision import CanCreate, IsModerator, IsOwner

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
            serializer.save(user=self.request.user)
        
    def update(self, request, *args, **kwargs):
        
        subs = Subscription.objects.filter(user=request.user)
        emails = get_users_emails_from_subs(subs)
        send_course_update_email.delay(emails)
        
        return super().update(request, *args, **kwargs)

    def get_queryset(self):

        if self.request.user.groups.filter(name='moderator').exists():
            return Course.objects.all()

        return Course.objects.filter(user=self.request.user)

    def get_permissions(self):

        permission_classes = (IsAuthenticated, )

        if self.action == 'create':
            permission_classes = (CanCreate, )

        elif self.action == 'destroy':
            permission_classes = (CanCreate, IsOwner)

        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = (IsModerator | IsOwner, )

        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, CanCreate, AllowAny)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if self.request.user.groups.filter(name='moderator').exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(user=self.request.user)

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated| IsOwner | IsModerator,)

    def get_queryset(self):

        if self.request.user.groups.filter(name='moderator').exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(user=self.request.user)

class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated | IsOwner | IsModerator,)

class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated | IsOwner,)


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]
    

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('course_name', 'lesson_name', 'payment_type')
    ordering_fields = ('date_of_payment', )