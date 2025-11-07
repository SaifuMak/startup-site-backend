from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from django.db.models import Q
from .models import Website, CommingSoonSites
from .serializers import WebsiteResponseSerializer, CommingSoonResponseSerializer

def _normalize_host(host: str) -> str:
    return (host or "").strip().lower()

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def site_by_host(request, host: str):
    host = _normalize_host(host)
    # print(host, '-----------------------')

    site_type = None
    site = None
    payload = {}

    site = Website.objects.filter(
        Q(primary_domain=host) |
        Q(domains__contains=[{"domain": host, "verified": True}])
    ).first()
    if site:
        site_type = "website"
        payload = WebsiteResponseSerializer(site).data

    if not site:
        site = CommingSoonSites.objects.filter(
            Q(primary_domain=host) |
            Q(domains__contains=[{"domain": host, "verified": True}])
        ).first()
        if site:
            site_type = "comming_soon_site"
            payload = CommingSoonResponseSerializer(site).data
  
  
    if not site and (host.startswith("localhost") or host.startswith("127.")):
        site = Website.objects.order_by("id").first()
        site_type = "website"
        payload = WebsiteResponseSerializer(site).data if site else {}

    if not site:
        return Response({"error": "site not found"}, status=status.HTTP_404_NOT_FOUND)

    # Add site type in response
    payload["site_type"] = site_type

    return Response(payload, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([permissions.IsAdminUser])
def switch_template(request, site_id: int):
    key = request.data.get("templateKey")
    if not key:
        return Response({"error": "templateKey required"}, status=400)
    try:
        site = Website.objects.get(pk=site_id)
        site.template_key = key
        site.save(update_fields=["template_key", "updated_at"])
        return Response({"ok": True, "templateKey": key})
    except Website.DoesNotExist:
        return Response({"error": "site not found"}, status=404)
