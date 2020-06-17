from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from axians_netbox_pdu.models import PDUConfig, PDUStatus
from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, PowerOutletTemplate, Site
from users.models import Token


class PDUStatusTestCase(TestCase):
    """Test the PDUStatus API."""

    def setUp(self):
        """Create a superuser and token for API calls."""
        self.user = User.objects.create(username="testuser", is_superuser=True)
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        self.base_url_lookup = "plugins-api:axians_netbox_pdu-api:pdustatus"

        self.site = Site.objects.create(name="Site", slug="site")
        self.role = DeviceRole.objects.create(name="Role", slug="role")
        self.manufacturer = Manufacturer.objects.create(name="Manufacturer", slug="manufacturer")
        self.device_type = DeviceType.objects.create(
            slug="device_type", model="device_type", manufacturer=self.manufacturer
        )
        self.outlets = PowerOutletTemplate.objects.create(device_type=self.device_type, name="1")
        self.pduconfig = PDUConfig.objects.create(
            device_type=self.device_type, power_usage_oid="1.1.1.1", power_usage_unit="watts"
        )
        self.device = Device.objects.create(
            name="Device One", device_role=self.role, device_type=self.device_type, site=self.site,
        )
        self.pdustatus = PDUStatus.objects.create(device=self.device, power_usage="1234")
        self.device_1 = Device.objects.create(
            name="Device Two", device_role=self.role, device_type=self.device_type, site=self.site,
        )
        self.pdustatus_1 = PDUStatus.objects.create(device=self.device_1, power_usage=4321)

    def test_list_pdustatus(self):
        """Verify that PDUStatus can be listed."""
        url = reverse(f"{self.base_url_lookup}-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_get_pdustatus(self):
        """Verify that an PDUStatus can be retrieved."""
        url = reverse(f"{self.base_url_lookup}-detail", kwargs={"pk": self.pdustatus.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["power_usage"], int(self.pdustatus.power_usage))

    def test_create_pdustatus_missing_mandatory_parameters(self):
        """Verify that the only mandatory POST parameters are power_usage_oid and power_usage_unit."""
        url = reverse(f"{self.base_url_lookup}-list")

        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # The response tells us which fields are missing from the request
        self.assertIn("device", response.data)
        self.assertIn("power_usage", response.data)
        self.assertEqual(len(response.data), 2, "Only two parameters should be mandatory")

    def test_create_pdustatus_duplicate(self):
        """Verify that you cannot add two instances."""
        url = reverse(f"{self.base_url_lookup}-list")
        power_usage = 1234
        data = {"device": self.device.pk, "power_usage": power_usage}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_pdustatus(self):
        """Verify that an PDUStatus can be updated via this API."""
        url = reverse(f"{self.base_url_lookup}-detail", kwargs={"pk": self.pdustatus.pk})

        response = self.client.patch(url, {"device": self.device.pk, "power_usage": "6666"}, format="json",)

        pdu_status = PDUStatus.objects.get(pk=self.pdustatus.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(pdu_status.device.pk, self.device.pk)
        self.assertEqual(pdu_status.power_usage, 6666)

        url = reverse(f"{self.base_url_lookup}-detail", kwargs={"pk": self.pdustatus_1.pk})

        response = self.client.patch(url, {"device": self.device_1.pk, "power_usage": "7777"}, format="json",)

        pdu_status = PDUStatus.objects.get(pk=self.pdustatus_1.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(pdu_status.device.pk, self.device_1.pk)
        self.assertEqual(pdu_status.power_usage, 7777)

    def test_delete_pdustatus(self):
        """Verify that an PDUStatus can be deleted."""
        url = reverse(f"{self.base_url_lookup}-detail", kwargs={"pk": self.pdustatus.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(PDUStatus.DoesNotExist):
            PDUStatus.objects.get(pk=self.pdustatus.pk)


class PDUStatusCreateTestCase(TestCase):
    """Test the PDUStatus API."""

    def setUp(self):
        """Create a superuser and token for API calls."""
        self.user = User.objects.create(username="testuser", is_superuser=True)
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        self.base_url_lookup = "plugins-api:axians_netbox_pdu-api:pdustatus"

        self.site = Site.objects.create(name="Site", slug="site")
        self.role = DeviceRole.objects.create(name="Role", slug="role")
        self.manufacturer = Manufacturer.objects.create(name="Manufacturer", slug="manufacturer")
        self.device_type = DeviceType.objects.create(
            slug="device_type", model="device_type", manufacturer=self.manufacturer
        )
        self.outlets = PowerOutletTemplate.objects.create(device_type=self.device_type, name="1")
        self.pduconfig = PDUConfig.objects.create(
            device_type=self.device_type, power_usage_oid="1.1.1.1", power_usage_unit="watts"
        )
        self.device = Device.objects.create(
            name="Device One", device_role=self.role, device_type=self.device_type, site=self.site,
        )

    def test_create_pdustatus(self):
        """Verify that an PDUStatus can be created."""
        url = reverse(f"{self.base_url_lookup}-list")
        power_usage = 1234
        data = {"device": self.device.pk, "power_usage": power_usage}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in data.items():
            self.assertEqual(response.data[key], value)
        self.assertEqual(response.data["device"], self.device.pk)
        self.assertEqual(response.data["power_usage"], power_usage)

        pdu_status = PDUStatus.objects.get(pk=response.data["id"])
        self.assertEqual(pdu_status.device.pk, data["device"])
        self.assertEqual(pdu_status.power_usage, data["power_usage"])

    def test_create_pdustatus_without_power_outlets(self):
        """Verify that an PDUStatus can be created."""

        self.device.poweroutlets.all().delete()

        url = reverse(f"{self.base_url_lookup}-list")
        power_usage = 1234
        data = {"device": self.device.pk, "power_usage": power_usage}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_pdustatus_without_device(self):
        """Verify that an PDUStatus can be created."""

        self.device.delete()

        url = reverse(f"{self.base_url_lookup}-list")
        power_usage = 1234
        data = {"device": 1, "power_usage": power_usage}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
