import uuid
from django.db import models

class Request(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='products')
    serial_number = models.IntegerField()
    product_name = models.CharField(max_length=255)
    input_image_urls = models.JSONField()  # Store a list of image URLs
    output_image_urls = models.JSONField(default=list)  # Store processed images
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
