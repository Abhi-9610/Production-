from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'company_name', 'client_name', 'progress', 'order_date', 'deadline_date')
    search_fields = ('company_name', 'client_name', 'order_id')
