from django.urls import path

from .views import (
    PDUConfigBulkDeleteView,
    PDUConfigCreateView,
    PDUConfigEditView,
    PDUConfigImportView,
    PDUConfigListView,
)

app_name = "axians_netbox_pdu"

urlpatterns = [
    path("pdu-config/", PDUConfigListView.as_view(), name="pduconfig_list"),
    path("pdu-config/add/", PDUConfigCreateView.as_view(), name="pduconfig_add"),
    path("pdu-config/import/", PDUConfigImportView.as_view(),
         name="pduconfig_import"),
    path("pdu-config/<int:pk>/delete/", PDUConfigBulkDeleteView.as_view(),
         name="pduconfig_bulk_delete"),
    path("pdu-config/<int:pk>/edit/",
         PDUConfigEditView.as_view(), name="pduconfig_edit"),
]
