from django.core.exceptions import ObjectDoesNotExist

from extras.plugins import PluginTemplateExtension


class DevicePDUStatus(PluginTemplateExtension):
    model = "dcim.device"

    def left_page(self):
        device = self.context["object"]
        try:
            pdustatus = device.pdustatus
            return self.render("axians_netbox_pdu/device_power_usage.html", extra_context={"pdustatus": pdustatus})
        except ObjectDoesNotExist:
            return ""


template_extensions = [DevicePDUStatus]
