from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from axians_netbox_pdu.choices import PDUUnitChoices
from axians_netbox_pdu.models import PDUConfig, PDUStatus
from dcim.models import Device, DeviceType


class PDUConfigSerializer(serializers.ModelSerializer):
    """Serializer for the PDUConfig model."""

    device_type = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        queryset=DeviceType.objects.filter(poweroutlet_templates__isnull=False).distinct(),
        slug_field="slug",
        required=True,
        help_text="Netbox DeviceType 'slug' value",
        validators=[UniqueValidator(queryset=PDUConfig.objects.all())],
    )

    power_usage_oid = serializers.CharField(required=True, help_text="OID string to collect power usage",)

    power_usage_unit = serializers.ChoiceField(
        choices=PDUUnitChoices.CHOICES, help_text="The unit of power to be collected",
    )

    class Meta:
        model = PDUConfig
        fields = [
            "id",
            "device_type",
            "power_usage_oid",
            "power_usage_unit",
        ]


class PDUStatusSerializer(serializers.ModelSerializer):
    """Serializer for the PSUStatus model."""

    device = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=Device.objects.filter(device_type__poweroutlet_templates__isnull=False).distinct(),
        validators=[UniqueValidator(queryset=PDUStatus.objects.all())],
        required=True,
        help_text="Netbox Device 'id' value",
    )

    power_usage = serializers.IntegerField(read_only=False, required=True, help_text="Power Usage Value")

    class Meta:
        model = PDUStatus
        fields = [
            "id",
            "device",
            "power_usage"
        ]
