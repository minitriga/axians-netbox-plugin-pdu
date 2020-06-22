import logging
from datetime import datetime

import django_rq
from django.conf import settings
from django_rq.management.commands import rqscheduler

from axians_netbox_pdu.worker import collect_power_usage_info

config = settings.PLUGINS_CONFIG["axians_netbox_pdu"]
scheduler = django_rq.get_scheduler()
log = logging.getLogger(__name__)


def clear_scheduled_jobs():
    """Delete any existing jobs in the scheduler when the app starts up """
    for job in scheduler.get_jobs():
        log.debug("Deleting scheduled job %s", job)
        job.delete()


def register_scheduled_jobs():
    """Do scheduling here"""
    if config["schedule"]:
        scheduler.schedule(
            scheduled_time=datetime.utcnow(), func=collect_power_usage_info, interval=config["schedule_interval"]
        )


class Command(rqscheduler.Command):
    def handle(self, *args, **kwargs):
        """This is necessary to prevent dupes"""
        clear_scheduled_jobs()
        register_scheduled_jobs()
        super(Command, self).handle(*args, **kwargs)
