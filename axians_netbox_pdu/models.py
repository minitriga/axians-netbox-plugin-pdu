from django.db import models

from .choices import PDUUnitChoices


class PDUConfig(models.Model):
    """PDU Configuration is contained within this model."""

    device_type = models.OneToOneField(to="dcim.DeviceType", on_delete=models.CASCADE, blank=True, null=True)

    power_usage_oid = models.CharField(
        max_length=255, help_text="OID string to collect power usage", blank=True, null=True
    )

    power_usage_unit = models.CharField(
        max_length=255, choices=PDUUnitChoices, help_text="The unit of power to be collected"
    )

    csv_headers = ["device_type", "power_usage_oid", "power_usage_unit"]

    def __str__(self):
        """String representation of an OnboardingTask."""
        return f"{self.device_type}"


class PDUStatus(models.Model):
    """PDU Status is contained within this model."""

    device = models.OneToOneField(to="dcim.Device", on_delete=models.CASCADE, blank=True, null=True)

    power_usage = models.PositiveSmallIntegerField(blank=True, null=True, help_text="Current PDU Power Usage")

    updated_at = models.DateTimeField(auto_now=True)

    def get_power_usage(self):
        return f"{self.power_usage} {dict(PDUUnitChoices.CHOICES)[self.device.device_type.pduconfig.power_usage_unit]}"

    def get_power_usage_watts(self):
        if self.device.device_type.pduconfig.power_usage_unit == PDUUnitChoices.UNIT_KILOWATTS:
            return self.power_usage * 1000
        else:
            return self.power_usage

    def get_power_usage_kilowatts(self):
        if self.device.device_type.pduconfig.power_usage_unit == PDUUnitChoices.UNIT_WATTS:
            return self.power_usage / 1000
        else:
            return self.power_usage
