from django.db import models

from .choices import PDUUnitChoices


class PDUConfig(models.Model):
    """PDU Configuration is contained within this model."""

    device_type = models.OneToOneField(to="dcim.DeviceType", on_delete=models.CASCADE, blank=True, null=True)

    power_usage_oid = models.CharField(
        max_length=255, help_text="OID string to collect power usage", blank=True, null=True
    )

    power_usage_unit = models.CharField(
        max_length=255, choices=PDUUnitChoices, help_text="The unit of power that will be collected"
    )

    csv_headers = ["device_type", "power_usage_oid", "power_usage_unit"]

    def __str__(self):
        """String representation of an OnboardingTask."""
        return f"{self.device_type}"
