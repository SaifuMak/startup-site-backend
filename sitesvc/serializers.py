from rest_framework import serializers
from .models import Website

class SiteSettingsSerializer(serializers.Serializer):
    siteId = serializers.CharField(source="id")
    templateKey = serializers.CharField(source="template_key")
    seo = serializers.SerializerMethodField()
    faviconUrl = serializers.SerializerMethodField()
    themeTokens = serializers.SerializerMethodField(required=False)

    logo = serializers.SerializerMethodField()
    colorScheme = serializers.SerializerMethodField()
    headerCodes = serializers.SerializerMethodField()
    socialLinks = serializers.SerializerMethodField()
    analyticsCode = serializers.SerializerMethodField()
    copyrightText = serializers.SerializerMethodField()
    theme = serializers.SerializerMethodField()
    footer_color = serializers.SerializerMethodField()
    header_color = serializers.SerializerMethodField()

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
    
    def get_logo(self, obj):
        s = obj.settings or {}
        return s.get("logo")

    def get_colorScheme(self, obj):
        s = obj.settings or {}
        return s.get("color_scheme")

    def get_headerCodes(self, obj):
        s = obj.settings or {}
        return s.get("header_codes")

    def get_socialLinks(self, obj):
        s = obj.settings or {}
        return s.get("social_links", [])

    def get_analyticsCode(self, obj):
        s = obj.settings or {}
        return s.get("analytics_code")

    def get_copyrightText(self, obj):
        s = obj.settings or {}
        return s.get("copyright_text")
    
    def get_theme(self, obj):
        s = obj.settings or {}
        return s.get("theme")
    
    def get_footer_color(self, obj):
        s = obj.settings or {}
        return s.get("footer_color")
    
    def get_header_color(self, obj):
        s = obj.settings or {}
        return s.get("header_color")




class WebsiteResponseSerializer(serializers.Serializer):
    settings = SiteSettingsSerializer(source="*")
    content = serializers.SerializerMethodField()
    clients = serializers.JSONField(read_only=True)
    faq = serializers.JSONField(read_only=True)


    def get_content(self, obj: Website):
        banners = obj.banner or [] 
        hero_banners = [
        {
            "title": banner.get("banner_title"),
            "subtitle": banner.get("banner_desc"),
            "image": banner.get("banner_img"),
            "cta": banner.get("banner_btn"),
        }
        for banner in banners
    ]
        return {
            "menu": (obj.settings or {}).get("menu", []),
            "hero": hero_banners, 
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
            "team" : obj.team or {},
            "clients": obj.clients or {},
            "faq": obj.faq or {}, 
        }
