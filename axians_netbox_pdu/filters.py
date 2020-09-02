import django_filters
from django.db.models import Q

from dcim.models import Device, DeviceType, Manufacturer
from utilities.filters import NameSlugSearchFilterSet

from .models import PDUConfig, PDUStatus


class PDUConfigFilter(NameSlugSearchFilterSet):
    """Filter PDUConfig instances."""

    q = django_filters.CharFilter(method="search", label="Search",)

    manufacturer = django_filters.ModelMultipleChoiceFilter(
        field_name="device_type__manufacturer__slug",
        queryset=Manufacturer.objects.filter(device_types__poweroutlettemplates__isnull=False).distinct(),
        to_field_name="slug",
        label="Manufacturer",
    )
    device_type = django_filters.ModelMultipleChoiceFilter(
        field_name="device_type__slug",
        queryset=DeviceType.objects.filter(poweroutlettemplates__isnull=False).distinct(),
        to_field_name="slug",
        label="Device Type",
    )

    class Meta:
        model = PDUConfig
        fields = ["id", "device_type", "manufacturer"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""

        if not value.strip():
            return queryset
        qs_filter = (
            Q(id__icontains=value)
            | Q(device_type__slug__icontains=value)
            | Q(device_type__manufacturer__slug__icontains=value)
        )
        return queryset.filter(qs_filter)


class PDUStatusFilter(NameSlugSearchFilterSet):
    """Filter PDUStatus instances."""

    q = django_filters.CharFilter(method="search", label="Search",)

    device = django_filters.ModelMultipleChoiceFilter(
        field_name="device__name",
        queryset=Device.objects.filter(device_type__poweroutlettemplates__isnull=False).distinct(),
        to_field_name="name",
        label="Device",
    )

    class Meta:
        model = PDUStatus
        fields = ["id", "device"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""

        if not value.strip():
            return queryset
        qs_filter = Q(id__icontains=value) | Q(device__name__icontains=value)
        return queryset.filter(qs_filter)
