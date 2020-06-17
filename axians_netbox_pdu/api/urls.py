from rest_framework import routers

from .views import PDUConfigViewSet, PDUStatusViewSet

router = routers.DefaultRouter()

router.register(r"pdu-config", PDUConfigViewSet)
router.register(r"pdu-status", PDUStatusViewSet)

urlpatterns = router.urls
