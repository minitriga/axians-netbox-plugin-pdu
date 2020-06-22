__version__ = "0.0.1"

from extras.plugins import PluginConfig


class PDUConfig(PluginConfig):
    """Plugin configuration for the axians_netbox_pdu plugin."""

    name = "axians_netbox_pdu"
    verbose_name = "PDU Status"
    version = __version__
    author = "Alexander Gittings"
    description = "A plugin for NetBox to easily get PDU information."
    base_url = "pdu"
    required_settings = []
    min_version = "2.8.1"
    default_settings = {
        "rack_view_pdu_devices": True,
        "rack_view_usage_summary": True,
        "rack_view_summary_unit": "watts",
    }
    caching_config = {}


config = PDUConfig  # pylint:disable=invalid-name
