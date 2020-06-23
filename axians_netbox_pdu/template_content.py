from django.core.exceptions import ObjectDoesNotExist

from extras.plugins import PluginTemplateExtension

from .utilities import get_rack_power_utilization


class DevicePDUStatus(PluginTemplateExtension):
    model = "dcim.device"

    def left_page(self):
        device = self.context["object"]

        try:
            return self.render(
                "axians_netbox_pdu/device_power_usage.html", extra_context={"pdustatus": device.pdustatus}
            )
        except ObjectDoesNotExist:
            return ""


class RackPDUStatus(PluginTemplateExtension):
    model = "dcim.rack"

    def right_page(self):
        rack = self.context["object"]

        pdus = rack.devices.filter(rack=rack).exclude(pdustatus=None)

        if pdus:
            (
                total_available_power,
                total_power_usage,
                total_power_usage_percentage,
                total_power_usage_unit,
            ) = get_rack_power_utilization(rack)
            ## fix issues with device not habing available power

            return self.render(
                "axians_netbox_pdu/rack_power_usage.html",
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

        try:
            return self.render(
                "axians_netbox_pdu/device_type_pduconfig.html", extra_context={"pduconfig": device_type.pduconfig}
            )
        except ObjectDoesNotExist:
            return ""


template_extensions = [DevicePDUStatus, RackPDUStatus, DeviceTypePDUConfig]
