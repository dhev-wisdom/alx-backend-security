from ipware import get_client_ip
from .models import RequestLog, BlockedIP
from django.http import HttpResponseForbidden
from django.core.cache import cache
import logging
import ipinfo
import environ
import os
from pathlib import Path
env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR / ".env")

logger = logging.getLogger(__name__)

IPINFO_TOKEN = env("IPINFO_TOKEN")
ipinfo_handler = ipinfo.getHandler(IPINFO_TOKEN)

class IPLoggingMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, is_routable = get_client_ip(request)
        if ip is None:
            ip = "0.0.0.0"

        if BlockedIP.objects.filter(ip_address=ip).exists():
            logger.warning(f"Blocked request from ip {ip}")
            return HttpResponseForbidden("Your IP has been blocked!")
        
        cache_key = f"geo_{ip}"
        geo_data = cache.get(cache_key)

        if not geo_data:
            try:
                details = ipinfo_handler.getDetails(ip)
                geo_data = {
                    "country": details.country_name if hasattr(details, "country_name") else None,
                    "city": details.city if hasattr(details, "city") else None
                }
                cache.set(cache_key, geo_data, timeout=60*60*24)
            except Exception as e:
                logger.error(f"Geolocation lookup failed for {ip}: {e}")
                geo_data = {
                    "country": None,
                    "city": None
                }

        RequestLog.objects.create(
            ip_address=ip,
            path=request.path,
            country=geo_data.get("country"),
            city=geo_data.get("city")
        )

        logger.info(f"Request from {ip} ({geo_data.get("country")}, {geo_data.get("city")}) to {request.path}")

        return self.get_response(request)
    