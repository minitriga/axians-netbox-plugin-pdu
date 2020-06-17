from django.urls import path

from .views import PDUConfigBulkDeleteView, PDUConfigCreateView, PDUConfigImportView, PDUConfigListView

urlpatterns = [
    path("", PDUConfigListView.as_view(), name="pduconfig_list"),
    path("add/", PDUConfigCreateView.as_view(), name="pduconfig_add"),
    path("import/", PDUConfigImportView.as_view(), name="pduconfig_import"),
    path("delete/", PDUConfigBulkDeleteView.as_view(), name="pduconfig_bulk_delete"),
]
