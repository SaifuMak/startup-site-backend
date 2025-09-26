from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from django.db.models import Q
from .models import Website
from .serializers import WebsiteResponseSerializer

def _normalize_host(host: str) -> str:
    return (host or "").strip().lower()

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def site_by_host(request, host: str):
    host = _normalize_host(host)
    # print(host, '-----------------------')
    site = (
        Website.objects
        .filter(Q(primary_domain=host) | Q(domains__contains=[{"domain": host, "verified": True}]))
        .first()
    )
    # print(site, '-----------------------')

    if not site:
        if host.startswith("localhost") or host.startswith("127."):
            site = Website.objects.order_by("id").first()
        if not site:
            return Response({"error": "site not found"}, status=status.HTTP_404_NOT_FOUND)

    payload = WebsiteResponseSerializer(site).data
    # print(payload)
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
