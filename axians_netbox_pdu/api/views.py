from rest_framework import mixins, viewsets

from axians_netbox_pdu.filters import PDUConfigFilter, PDUStatusFilter
from axians_netbox_pdu.models import PDUConfig, PDUStatus

from .serializers import PDUConfigSerializer, PDUStatusSerializer


class PDUConfigViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):

    """CRUD PDUConfig instances"""

    queryset = PDUConfig.objects.all()
    filterset_class = PDUConfigFilter
    serializer_class = PDUConfigSerializer


class PDUStatusViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """CRUD PDUStatus Instances"""

    queryset = PDUStatus.objects.all()
    filterset_class = PDUStatusFilter
    serializer_class = PDUStatusSerializer
