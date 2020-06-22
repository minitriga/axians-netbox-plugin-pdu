from django.conf import settings
from django.db.models import Sum

from dcim.models import PowerFeed

from .choices import PDUUnitChoices
from .models import PDUStatus


def get_rack_power_utilization(rack):
    """ Determine the utilization of power in a rack and return it as a percentage."""

    config_unit = settings.PLUGINS_CONFIG["axians_netbox_pdu"]["rack_view_summary_unit"]

    total_available_power = None
    total_power_usage = None
    total_power_usage_percentage = None
    total_power_usage_unit = config_unit
    power_results = []

    used_power = PDUStatus.objects.filter(device__rack=rack)
    available_power = PowerFeed.objects.filter(rack=rack).values("available_power")

    # work out available power
    if available_power:
        total_available_power = sum(x["available_power"] for x in available_power)

    # work out power_usage
    total_power_usage = sum(x.get_power_usage_watts() for x in used_power)

    # work out percentage used
    if total_available_power:
        total_power_usage_percentage = int(total_power_usage / total_available_power * 100) or 0

    # Determine if we are using watts or kilowatts
    if config_unit in dict(PDUUnitChoices.TEMPLATE_CHOICES):
        if config_unit == PDUUnitChoices.UNIT_KILOWATTS:
            # if we are using kilowats do the math
            total_available_power = total_available_power / 1000
            total_power_usage = total_power_usage / 1000
    else:
        total_power_usage_unit = PDUUnitChoices.UNIT_WATTS

    # return rack power usage
    return total_available_power, total_power_usage, total_power_usage_percentage, total_power_usage_unit
