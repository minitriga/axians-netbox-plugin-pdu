import logging
from datetime import datetime

import django_rq
from django.conf import settings
from django_rq import job

from dcim.models import Device
from easysnmp import EasySNMPError, snmp_get

from .models import PDUConfig, PDUStatus

logger = logging.getLogger("rq.worker")
logger.setLevel(logging.DEBUG)


@job
def collect_power_usage_info():
    config = settings.PLUGINS_CONFIG["axians_netbox_pdu"]
    devices = Device.objects.filter().exclude(device_type__pduconfig__isnull=True).exclude(primary_ip4__isnull=True)

    logging.info("Start: Collecting Power Usage Information")
    results = []
    for device in devices:
        try:
            power_usage = snmp_get(
                device.device_type.pduconfig.power_usage_oid,
                hostname=str(device.primary_ip4.address.ip),
                community=config["snmp_read"],
                version=2,
            )
        except EasySNMPError as err:
            logging.error(f"Failed to get power usage status for {device.name}: {err}.")
            raise

        pdu_status = PDUStatus.objects.update_or_create(device=device, defaults={"power_usage": power_usage.value})

        data = {device.name: power_usage.value}

        results.append(data)

    logging.info("FINISH: Collecting Power Usage Information")
    return results
