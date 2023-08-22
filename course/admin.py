from django.contrib import admin
from course.models import Payment

@admin.register(Payment)
class PayAdmin(admin.ModelAdmin):
    list_display = ("date_of_payment", "pay_sum", "payment_type")  # отображение на дисплее
    list_filter = ("date_of_payment", "pay_sum", "payment_type")  # фильтр
    search_fields = ("date_of_payment", "pay_sum", "payment_type")  # поля поиска

