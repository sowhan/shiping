"""
Background Workers - Celery Configuration
Distributed task processing for background operations.
"""

from celery import Celery

from app.core.config import settings

# Celery configuration
celery_app = Celery(
    "maritime_workers",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=[
        "app.workers.route_calculator",
        "app.workers.data_updater",
    ]
)

# Celery settings
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes max
    task_soft_time_limit=240,  # 4 minutes soft limit
    worker_prefetch_multiplier=1,
    worker_concurrency=4,
)

# Task routes
celery_app.conf.task_routes = {
    "app.workers.route_calculator.*": {"queue": "route_calculations"},
    "app.workers.data_updater.*": {"queue": "data_updates"},
}

# Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    "update-port-data": {
        "task": "app.workers.data_updater.update_port_data",
        "schedule": 86400,  # Daily
    },
    "cleanup-expired-routes": {
        "task": "app.workers.data_updater.cleanup_expired_routes",
        "schedule": 3600,  # Hourly
    },
}
