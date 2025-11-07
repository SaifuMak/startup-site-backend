from django.contrib import admin
from .models import Website, Payment, CommingSoonSites

@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ("id", "primary_domain", "owner", "template_key", "status", "updated_at")
    search_fields = ("primary_domain", "owner__email")
    list_filter = ("status", "template_key", "updated_at")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "website", "provider", "amount_inr", "status", "created_at")
    search_fields = ("provider_id", "user__email")
    list_filter = ("status", "provider", "created_at")



# admin.site.register(CommingSoonSites)


@admin.register(CommingSoonSites)
class CommingSoonSitesAdmin(admin.ModelAdmin):
    list_display = ("id", "primary_domain", "owner", "template_key", "status", "updated_at")