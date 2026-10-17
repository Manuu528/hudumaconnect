from django.db import models

# Create your models here.

import uuid

from django.conf import settings
from django.db import models


class ServiceRequest(models.Model):
    CATEGORY_CHOICES = [
        ("water", "Water Supply"),
        ("streetlight", "Broken Streetlight"),
        ("garbage", "Garbage Collection"),
        ("roads", "Road Damage"),
        ("drainage", "Drainage and Sewage"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
    ]

    reference_number = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    citizen = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="service_requests",
    )
    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
    )
    location = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(
        upload_to="service_requests/",
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reference_number} - {self.get_category_display()}"

