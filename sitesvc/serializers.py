from rest_framework import serializers
from .models import Website

class SiteSettingsSerializer(serializers.Serializer):
    siteId = serializers.CharField(source="id")
    templateKey = serializers.CharField(source="template_key")
    seo = serializers.SerializerMethodField()
    faviconUrl = serializers.SerializerMethodField()
    themeTokens = serializers.SerializerMethodField(required=False)

    def get_seo(self, obj):
        s = obj.settings or {}
        return {
            "title": s.get("meta_title"),
            "description": s.get("meta_description"),
            "ogImage": s.get("og_image"),
        }

    def get_faviconUrl(self, obj):
        s = obj.settings or {}
        return s.get("favicon")

    def get_themeTokens(self, obj):
        s = obj.settings or {}
        return s.get("theme_tokens")

class WebsiteResponseSerializer(serializers.Serializer):
    settings = SiteSettingsSerializer(source="*")
    content = serializers.SerializerMethodField()

    def get_content(self, obj: Website):
        return {
            "menu": (obj.settings or {}).get("menu", []),
            "hero": {
                "title": (obj.banner or {}).get("banner_title"),
                "subtitle": (obj.banner or {}).get("banner_desc"),
                "image": (obj.banner or {}).get("banner_img"),
                "cta": (obj.banner or {}).get("banner_btn"),
            },
            "about": {
                "heading": (obj.about or {}).get("abt_title"),
                "body": (obj.about or {}).get("abt_desc"),
                "image": (obj.about or {}).get("abt_img"),
            },
            "services": obj.services or {},
            "products": obj.products or {},
            "gallery": obj.gallery or {},
            "testimonials": (obj.settings or {}).get("testimonials", {}),
            "cta": (obj.settings or {}).get("cta", {}),
            "footer": (obj.settings or {}).get("footer", {}),
            "contact": obj.contact or {},
        }
