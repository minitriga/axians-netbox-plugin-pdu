from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link="plugins:axians_netbox_pdu:pduconfig_list",
        link_text="PDU Config",
        permissions=["axians_netbox_pdu.view_pduconfig"],
        buttons=(
            PluginMenuButton(
                link="plugins:axians_netbox_pdu:pduconfig_add",
                title="Add",
                icon_class="fa fa-plus",
                color=ButtonColorChoices.GREEN,
                permissions=["axians_netbox_pdu.add_pduconfig"],
            ),
            PluginMenuButton(
                link="plugins:axians_netbox_pdu:pduconfig_import",
                title="Bulk Add",
                icon_class="fa fa-download",
                color=ButtonColorChoices.BLUE,
                permissions=["axians_netbox_pdu.add_pduconfig"],
            ),
        ),
    ),
)
