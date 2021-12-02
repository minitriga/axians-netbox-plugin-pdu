from django.core.exceptions import ObjectDoesNotExist

from extras.plugins import PluginTemplateExtension

from .utilities import get_rack_power_utilization

from django.conf import settings
from packaging import version

NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)

class DevicePDUStatus(PluginTemplateExtension):
    model = "dcim.device"

    def left_page(self):
        device = self.context["object"]

        template_filename = ""
        if NETBOX_CURRENT_VERSION >= version.parse("3.0"):
            template_filename = "axians_netbox_pdu/device_power_usage_3_x.html"
        else:
            template_filename = "axians_netbox_pdu/device_power_usage.html"

        try:
            return self.render(
                template_filename, extra_context={"pdustatus": device.pdustatus}
            )
        except ObjectDoesNotExist:
            return ""


class RackPDUStatus(PluginTemplateExtension):
    model = "dcim.rack"

    def right_page(self):
        rack = self.context["object"]

        pdus = rack.devices.filter(rack=rack).exclude(pdustatus=None)

        template_filename = ""
        if NETBOX_CURRENT_VERSION >= version.parse("3.0"):
            template_filename = "axians_netbox_pdu/rack_power_usage_3_x.html"
        else:
            template_filename = "axians_netbox_pdu/rack_power_usage.html"

        if pdus:
            (
                total_available_power,
                total_power_usage,
                total_power_usage_percentage,
                total_power_usage_unit,
            ) = get_rack_power_utilization(rack)
            ## fix issues with device not habing available power

            return self.render(
                template_filename,
                extra_context={
                    "pdus": pdus,
                    "total_power_usage": total_power_usage,
                    "total_available_power": total_available_power,
                    "total_power_usage_percentage": total_power_usage_percentage,
                    "total_power_usage_unit": total_power_usage_unit,
                },
            )
        else:
            return ""


class DeviceTypePDUConfig(PluginTemplateExtension):
    model = "dcim.devicetype"

    def right_page(self):
        device_type = self.context["object"]

        template_filename = ""
        if NETBOX_CURRENT_VERSION >= version.parse("3.0"):
            template_filename = "axians_netbox_pdu/device_type_pduconfig_3_x.html"
        else:
            template_filename = "axians_netbox_pdu/device_type_pduconfig.html"

        try:
            return self.render(
                template_filename, extra_context={"pduconfig": device_type.pduconfig}
            )
        except ObjectDoesNotExist:
            return ""


template_extensions = [DevicePDUStatus, RackPDUStatus, DeviceTypePDUConfig]
