from ipware import get_client_ip
from .models import RequestLog, BlockedIP
from django.http import HttpResponseForbidden
import logging

logger = logging.getLogger(__name__)

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

        RequestLog.objects.create(ip_address=ip, path=request.path)

        logger.info(f"IP: {ip}, Path: {request.path}")

        return self.get_response(request)
    