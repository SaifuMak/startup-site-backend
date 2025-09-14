from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from sitesvc.models import Website

class Command(BaseCommand):
    help = "Seed a demo website"

    def handle(self, *args, **kwargs):
        user, _ = User.objects.get_or_create(username="demo", defaults={"email": "demo@example.com"})
        site, created = Website.objects.get_or_create(
            primary_domain="localhost:3000",
            owner=user,
            defaults={
                "template_key": "layout-1",
                "settings": {
                    "meta_title": "Acme Tools",
                    "meta_description": "Quality tools for makers",
                    "favicon": "",
                    "footer": {"columns": [{"title":"Company","links":[{"label":"About","href":"#about"}]}]},
                    "cta": {"heading":"Ready to start?","button":{"label":"Contact","href":"#contact"}},
                    "menu": [
                        {"label":"Home","href":"#home"},
                        {"label":"Services","href":"#services"},
                        {"label":"About","href":"#about"},
                        {"label":"Gallery","href":"#gallery"},
                        {"label":"Testimonials","href":"#testimonials"},
                        {"label":"Contact","href":"#contact"}
                    ]
                },
                "banner": {
                    "banner_title":"Welcome to Acme",
                    "banner_desc":"Built with Next.js templates",
                    "banner_img":"/images/hero.jpg",
                    "banner_btn":{"title":"Get Started","link":"#contact"},
                },
                "about": {
                    "abt_title":"About Acme",
                    "abt_desc":"We craft digital experiences.",
                    "abt_img":"/images/about.jpg",
                },
                "services": {
                    "service_title":"Our Services",
                    "service_desc":"What we do best",
                    "service_items":[
                        {"name":"Design","desc":"UI/UX & brand"},
                        {"name":"Development","desc":"Next.js + Django"},
                        {"name":"SEO","desc":"Get found online"}
                    ],
                },
                "gallery": {
                    "gallery_items":[
                        {"name":"Proj 1","title":"Kitchen","img":"/images/g1.jpg"},
                        {"name":"Proj 2","title":"Workshop","img":"/images/g2.jpg"}
                    ]
                },
                "contact": {
                    "contact_title":"Contact",
                    "contact_desc":"We’d love to hear from you.",
                    "contact_items":[{"icon":"phone","title":"Phone","desc":"7736101555","link":"tel:+917736101555"}]
                }
            }
        )
        self.stdout.write(self.style.SUCCESS(f"Seeded site id={site.id}, created={created}"))
