from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from axians_netbox_pdu.models import PDUConfig
from dcim.models import DeviceType, Manufacturer, PowerOutletTemplate
from users.models import Token


class PDUConfigTestCase(TestCase):
    """Test the PDUConfig API."""

    def setUp(self):
        """Create a superuser and token for API calls."""
        self.user = User.objects.create(username="testuser", is_superuser=True)
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        self.base_url_lookup = "plugins-api:axians_netbox_pdu-api:pduconfig"

        self.manufacturer = Manufacturer.objects.create(name="Test", slug="test")
        self.device_type = DeviceType.objects.create(slug="test", model="test", manufacturer=self.manufacturer)
        self.device_type_1 = DeviceType.objects.create(slug="test1", model="test1", manufacturer=self.manufacturer)
        self.outlets = PowerOutletTemplate.objects.create(device_type=self.device_type, name="1")
        self.outlets_1 = PowerOutletTemplate.objects.create(device_type=self.device_type_1, name="1")
        self.pduconfig_1 = PDUConfig.objects.create(
            device_type=self.device_type, power_usage_oid="1.1.1.1", power_usage_unit="watts"
        )
        self.pduconfig_2 = PDUConfig.objects.create(
            device_type=self.device_type_1, power_usage_oid="0.1.2.3", power_usage_unit="watts"
        )

    def test_list_pduconfig(self):
        """Verify that PDUConfig can be listed."""
        url = reverse(f"{self.base_url_lookup}-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_get_pduconfig(self):
        """Verify that an PDUConfig can be retrieved."""
        url = reverse(f"{self.base_url_lookup}-detail", kwargs={"pk": self.pduconfig_1.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["power_usage_oid"], self.pduconfig_1.power_usage_oid)
        self.assertEqual(response.data["power_usage_unit"], self.pduconfig_1.power_usage_unit)

    def test_create_pduconfig_missing_mandatory_parameters(self):
        """Verify that the only mandatory POST parameters are power_usage_oid and power_usage_unit."""
        url = reverse(f"{self.base_url_lookup}-list")

        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # The response tells us which fields are missing from the request
        self.assertIn("device_type", response.data)
        self.assertIn("power_usage_oid", response.data)
        self.assertIn("power_usage_unit", response.data)
        self.assertEqual(len(response.data), 3, "Only two parameters should be mandatory")

    def test_create_pduconfig_duplicate(self):
        """Verify that you cannot add two instances."""
        url = reverse(f"{self.base_url_lookup}-list")
        power_usage_oid = "1.2.3.4"
        power_usage_unit = "watts"
        data = {
            "device_type": self.device_type.slug,
            "power_usage_oid": power_usage_oid,
            "power_usage_unit": power_usage_unit,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_pduconfig(self):
        """Verify that an PDUConfig can be updated via this API."""
        url = reverse(f"{self.base_url_lookup}-detail", kwargs={"pk": self.pduconfig_1.pk})

        response = self.client.patch(
            url,
            {"device_type": self.device_type.slug, "power_usage_oid": "9.9.9.9", "power_usage_unit": "watts"},
            format="json",
        )
        pdu_config = PDUConfig.objects.get(pk=self.pduconfig_1.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.pduconfig_1.device_type.slug, self.device_type.slug)
        self.assertEqual(PDUConfig.objects.get(pk=self.pduconfig_1.pk).power_usage_oid, "9.9.9.9")
        self.assertEqual(PDUConfig.objects.get(pk=self.pduconfig_1.pk).power_usage_unit, "watts")

        url = reverse(f"{self.base_url_lookup}-detail", kwargs={"pk": self.pduconfig_2.pk})

        response = self.client.put(
            url,
            {"device_type": self.device_type_1.slug, "power_usage_oid": "8.8.8.8", "power_usage_unit": "watts"},
            format="json",
        )
        pdu_config = PDUConfig.objects.get(pk=self.pduconfig_2.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.pduconfig_2.device_type.slug, self.device_type_1.slug)
        self.assertEqual(pdu_config.power_usage_oid, "8.8.8.8")
        self.assertEqual(pdu_config.power_usage_unit, "watts")

    def test_delete_pduconfig(self):
        """Verify that an PDUConfig can be deleted."""
        url = reverse(f"{self.base_url_lookup}-detail", kwargs={"pk": self.pduconfig_1.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(PDUConfig.DoesNotExist):
            PDUConfig.objects.get(pk=self.pduconfig_1.pk)


class PDUConfigCreateTestCase(TestCase):
    """Test the PDUConfig API."""

    def setUp(self):
        """Create a superuser and token for API calls."""
        self.user = User.objects.create(username="testuser", is_superuser=True)
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        self.base_url_lookup = "plugins-api:axians_netbox_pdu-api:pduconfig"

        self.manufacturer = Manufacturer.objects.create(name="Test", slug="test")
        self.device_type = DeviceType.objects.create(slug="test", model="test", manufacturer=self.manufacturer)
        self.device_type_1 = DeviceType.objects.create(slug="test1", model="test1", manufacturer=self.manufacturer)
        self.outlets = PowerOutletTemplate.objects.create(device_type=self.device_type, name="1")
        self.outlets_1 = PowerOutletTemplate.objects.create(device_type=self.device_type_1, name="1")

    def test_create_pduconfig(self):
        """Verify that an PDUConfig can be created."""
        url = reverse(f"{self.base_url_lookup}-list")
        power_usage_oid = "1.2.3.4"
        power_usage_unit = "watts"
        data = {
            "device_type": self.device_type.slug,
            "power_usage_oid": power_usage_oid,
            "power_usage_unit": power_usage_unit,
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in data.items():
            self.assertEqual(response.data[key], value)
        self.assertEqual(response.data["device_type"], self.device_type.slug)
        self.assertEqual(response.data["power_usage_oid"], power_usage_oid)
        self.assertEqual(response.data["power_usage_unit"], power_usage_unit)

        pdu_config = PDUConfig.objects.get(pk=response.data["id"])
        self.assertEqual(pdu_config.device_type.slug, data["device_type"])
        self.assertEqual(pdu_config.power_usage_oid, data["power_usage_oid"])
        self.assertEqual(pdu_config.power_usage_unit, data["power_usage_unit"])
