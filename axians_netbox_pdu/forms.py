from django import forms

from dcim.models import DeviceType, Manufacturer
from extras.forms import CustomFieldModelCSVForm
from utilities.forms import BootstrapMixin

from .choices import PDUUnitChoices
from .models import PDUConfig

BLANK_CHOICE = (("", "---------"),)


class PDUConfigForm(BootstrapMixin, forms.ModelForm):
    """Form for creating a new PDUConfig"""

    device_type = forms.ModelChoiceField(
        queryset=DeviceType.objects.filter(poweroutlettemplates__isnull=False).distinct(),
        required=True,
        to_field_name="slug",
        label="Device Type",
    )

    power_usage_oid = forms.CharField(
        required=True, label="Power Usage OID", help_text="OID string to collect power usage"
    )

    power_usage_unit = forms.ChoiceField(
        choices=BLANK_CHOICE + PDUUnitChoices.CHOICES, required=True, label="Power Usage Unit"
    )

    class Meta:
        model = PDUConfig
        fields = ["device_type", "power_usage_oid", "power_usage_unit"]
        obj_type = "test"


class PDUConfigFilterForm(BootstrapMixin, forms.ModelForm):
    """Form for siltering PDUConfig instances."""

    device_type = forms.ModelChoiceField(
        queryset=DeviceType.objects.filter(poweroutlettemplates__isnull=False).distinct(),
        required=False,
        to_field_name="slug",
    )

    manufacturer = forms.ModelChoiceField(
        queryset=Manufacturer.objects.filter(device_types__poweroutlettemplates__isnull=False).distinct(),
        required=False,
        to_field_name="slug",
    )

    q = forms.CharField(required=False, label="Search")

    class Meta:
        model = PDUConfig
        fields = ["q", "device_type", "manufacturer"]


class PDUConfigCSVForm(CustomFieldModelCSVForm):
    """Form for entering CSV to bulk-import PDUConfig entries."""

    device_type = forms.ModelChoiceField(
        queryset=DeviceType.objects.filter(poweroutlettemplates__isnull=False).distinct(),
        required=True,
        to_field_name="slug",
        help_text="slug of device type",
        error_messages={"invalid_choice": "Device Type not found",},
    )

    power_usage_oid = forms.CharField(required=True, help_text="OID string to collect power usage")

    power_usage_unit = forms.CharField(required=True, help_text="The unit of power that will be collected")

    class Meta:
        model = PDUConfig
        fields = PDUConfig.csv_headers

    def save(self, commit=True, **kwargs):
        """Save the model"""
        model = super().save(commit=commit, **kwargs)
        return model
