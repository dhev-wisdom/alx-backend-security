from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db import models
from .models import RequestLog, SuspiciousIP

SENSITIVE_PATHS = ["/admin", "/login"]

@shared_task
def detect_anomalies():
    """
    Run every hour:
    - Flag IPs with >100 requests/hour
    - Flag IPs accessing sensitive paths
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # 1. Check request volume
    high_volume_ips = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        .values("ip_address")
        .annotate(request_count=models.Count("id"))
        .filter(request_count__gt=100)
    )

    for entry in high_volume_ips:
        ip = entry["ip_address"]
        reason = f"High request volume: {entry['request_count']} in the last hour"
        SuspiciousIP.objects.get_or_create(ip_address=ip, reason=reason)

    # 2. Check sensitive paths
    sensitive_logs = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago, path__in=SENSITIVE_PATHS
    )

    for log in sensitive_logs:
        reason = f"Accessed sensitive path: {log.path}"
        SuspiciousIP.objects.get_or_create(ip_address=log.ip_address, reason=reason)
