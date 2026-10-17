from django.contrib import admin

# Register your models here.




from django.contrib import admin
from .models import ServiceRequest


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = (
        "reference_number",
        "citizen",
        "category",
        "location",
        "status",
        "created_at",
    )
    list_filter = ("status", "category", "created_at")
    search_fields = (
        "location",
        "description",
        "citizen__username",
        "citizen__email",
    )
    list_editable = ("status",)
    readonly_fields = (
        "reference_number",
        "created_at",
        "updated_at",
    )

