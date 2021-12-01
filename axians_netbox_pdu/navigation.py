from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

from django.conf import settings
from packaging import version

NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)

if NETBOX_CURRENT_VERSION >= version.parse("3.0"):
    import_icon_class = "mdi mdi-upload"
else:
    import_icon_class = "mdi mdi-database-import-outline"

menu_items = (
    PluginMenuItem(
        link="plugins:axians_netbox_pdu:pduconfig_list",
        link_text="PDU Config",
        permissions=["axians_netbox_pdu.view_pduconfig"],
        buttons=(
            PluginMenuButton(
                link="plugins:axians_netbox_pdu:pduconfig_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["axians_netbox_pdu.add_pduconfig"],
            ),
            PluginMenuButton(
                link="plugins:axians_netbox_pdu:pduconfig_import",
                title="Bulk Add",
                icon_class=import_icon_class,
                color=ButtonColorChoices.CYAN,
                permissions=["axians_netbox_pdu.add_pduconfig"],
            ),
        ),
    ),
)
