from django.db import models
from django.utils.timezone import now
import random

def generate_order_id():
    return random.randint(10000, 99999)

class Order(models.Model):
    order_id = models.PositiveIntegerField(default=generate_order_id, unique=True, editable=False)
    company_name = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)
    salesperson_name = models.CharField(max_length=255)
    back_design = models.ImageField(upload_to='designs/', blank=True, null=True)
    front_design = models.ImageField(upload_to='designs/', blank=True, null=True)
    pocket_design = models.ImageField(upload_to='designs/', blank=True, null=True)
    sleeve_design = models.ImageField(upload_to='designs/', blank=True, null=True)
    design_Size=models.CharField(max_length=255, blank=True, null=True)
    product_list = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    remark = models.CharField(max_length=255,blank=True, null=True)
    order_date = models.DateField(default=now)  # Auto-filled with the current date
    deadline_date = models.DateField()
    completed_date = models.DateField(blank=True, null=True)
    progress = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ], default='Pending')

    def __str__(self):
        return f"Order {self.order_id}"
