import django_tables2 as tables

from utilities.tables import BaseTable, ToggleColumn

from .models import PDUConfig


class PDUConfigTable(BaseTable):
    """Table for displaying PDUConfig information"""

    pk = ToggleColumn()
    device_type = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = PDUConfig
        fields = (
            "pk",
            "device_type",
            "power_usage_oid",
            "power_usage_unit",
        )


class PDUConfigBulkTable(BaseTable):

    device_type = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = PDUConfig
        fields = (
            "pk",
            "device_type",
            "power_usage_oid",
            "power_usage_unit",
        )
