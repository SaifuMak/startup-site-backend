from django.db import models
from django.core.validators import MinValueValidator
from authentication.models import User

class Website(models.Model):
    STATUS_CHOICES = [("active", "active"), ("paused", "paused"), ("deleted", "deleted")]

    id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="websites", null=True, blank=True)
    primary_domain = models.CharField(max_length=255, unique=True, null=True, blank=True)
    domains = models.JSONField(default=list, blank=True)

    template_key = models.CharField(max_length=64, default="layout-1")
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="active")

    settings = models.JSONField(default=dict, blank=True)
    color_settings = models.JSONField(default=dict, blank=True, null=True)
    banner   = models.JSONField(default=dict, blank=True)
    about    = models.JSONField(default=dict, blank=True)
    services = models.JSONField(default=dict, blank=True)
    products = models.JSONField(default=dict, blank=True)
    gallery  = models.JSONField(default=dict, blank=True)
    clients  = models.JSONField(default=dict, blank=True)
    team     = models.JSONField(default=dict, blank=True)
    faq      = models.JSONField(default=dict, blank=True)
    contact  = models.JSONField(default=dict, blank=True)

    content_version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        svc_items = (self.services or {}).get("service_items", [])
        prod_items = (self.products or {}).get("products_items", [])
        if isinstance(svc_items, list) and len(svc_items) > 20:
            raise ValueError("service_items cannot exceed 20")
        if isinstance(prod_items, list) and len(prod_items) > 20:
            raise ValueError("products_items cannot exceed 20")

    def __str__(self):
        return f"{self.primary_domain or 'no-domain'} ({self.template_key})"


class CommingSoonSites(models.Model):
    STATUS_CHOICES = [("active", "active"), ("paused", "paused"), ("deleted", "deleted")]

    id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="cv_sites", null=True, blank=True)
    primary_domain = models.CharField(max_length=255, unique=True, null=True, blank=True)
    domains = models.JSONField(default=list, blank=True)

    template_key = models.CharField(max_length=64, default="layout-1")
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="active")

    settings = models.JSONField(default=dict, blank=True)
    color_settings = models.JSONField(default=dict, blank=True, null=True)
    contact  = models.JSONField(default=dict, blank=True)
    details = models.JSONField(default=dict, blank=True)

    content_version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.primary_domain or 'no-domain'} ({self.template_key})"



class Payment(models.Model):
    STATUS_CHOICES = [
        ("succeeded", "succeeded"),
        ("pending", "pending"),
        ("failed", "failed"),
        ("refunded", "refunded"),
    ]
    PROVIDER_CHOICES = [("razorpay", "razorpay"), ("stripe", "stripe"), ("manual", "manual")]

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="payments", null=True, blank=True)
    website = models.ForeignKey(Website, on_delete=models.SET_NULL, null=True, blank=True, related_name="payments")
    provider = models.CharField(max_length=32, choices=PROVIDER_CHOICES)
    provider_id = models.CharField(max_length=191, null=True, blank=True)
    amount_inr = models.IntegerField(validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=8, default="INR")
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider}:{self.provider_id} {self.status}"
