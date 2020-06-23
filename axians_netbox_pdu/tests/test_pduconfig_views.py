from django.contrib.auth.models import Permission, User
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from axians_netbox_pdu.models import PDUConfig
from dcim.models import DeviceType, Manufacturer, PowerOutletTemplate


class PDUConfigListViewTestCase(TestCase):
    """Test PDUConfig List View"""

    def setUp(self):
        """Create a user and baseline data for testing."""
        self.user = User.objects.create(username="testuser")
        self.client = Client()
        self.client.force_login(self.user)

        self.url = reverse("plugins:axians_netbox_pdu:pduconfig_list")

        self.manufacturer = Manufacturer.objects.create(name="Test", slug="test")
        self.device_type = DeviceType.objects.create(slug="test", model="test", manufacturer=self.manufacturer)
        self.outlets = PowerOutletTemplate.objects.create(device_type=self.device_type, name="1")

    @override_settings(EXEMPT_VIEW_PERMISSIONS=["*"])
    def test_list_pduconfig_anonymous(self):
        """Verify that PDUConfig can be listed without logging in if permissions are exempted."""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "axians_netbox_pdu/pduconfig_list.html")

    @override_settings(EXEMPT_VIEW_PERMISSIONS=[])
    def test_list_pduconfig(self):
        """Verify that PDUConfig can be listed by a user with appropriate permissions."""
        # Attempt to access without permissions
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

        # Add permission
        self.user.user_permissions.add(
            Permission.objects.get(content_type__app_label="axians_netbox_pdu", codename="view_pduconfig")
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "axians_netbox_pdu/pduconfig_list.html")


class PDUConfigCreateViewTestCase(TestCase):
    """Test the PDUConfigCreateView view."""

    def setUp(self):
        """Create a user and baseline data for testing."""
        self.user = User.objects.create(username="testuser")
        self.client = Client()
        self.client.force_login(self.user)

        self.url = reverse("plugins:axians_netbox_pdu:pduconfig_add")

        self.manufacturer = Manufacturer.objects.create(name="Test", slug="test")
        self.device_type = DeviceType.objects.create(slug="test", model="test", manufacturer=self.manufacturer)
        self.outlets = PowerOutletTemplate.objects.create(device_type=self.device_type, name="1")

    @override_settings(EXEMPT_VIEW_PERMISSIONS=["*"])
    def test_get_anonymous(self):
        """Verify that the view cannot be accessed by anonymous users even if permissions are exempted."""
        self.client.logout()
        response = self.client.get(self.url)
        # Redirected to the login page
        self.assertEqual(response.status_code, 302)

    @override_settings(EXEMPT_VIEW_PERMISSIONS=[])
    def test_get(self):
        """Verify that the view can be seen by a user with appropriate permissions."""
        # Attempt to access without permissions
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

        # Add permission
        self.user.user_permissions.add(
            Permission.objects.get(content_type__app_label="axians_netbox_pdu", codename="add_pduconfig")
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "axians_netbox_pdu/pduconfig_edit.html")

    @override_settings(EXEMPT_VIEW_PERMISSIONS=["*"])
    def test_post_anonymous(self):
        """Verify that the view cannot be accessed by anonymous users even if permissions are exempted."""
        self.client.logout()
        response = self.client.get(self.url)
        # Redirected to the login page
        self.assertEqual(response.status_code, 302)

    @override_settings(EXEMPT_VIEW_PERMISSIONS=[])
    def test_post(self):
        """Verify that the view can be used by a user with appropriate permissions."""
        # Attempt to access without permissions
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

        # Add permission
        self.user.user_permissions.add(
            Permission.objects.get(content_type__app_label="axians_netbox_pdu", codename="add_pduconfig")
        )

        response = self.client.post(
            self.url, data={"device_type": "test", "power_usage_oid": "1.1.1.1", "power_usage_unit": "watts"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PDUConfig.objects.count(), 1)


class PDUConfigEditViewTestCase(TestCase):
    """Test the PDUConfigEditView view."""

    def setUp(self):
        """Create a user and baseline data for testing."""
        self.user = User.objects.create(username="testuser")
        self.client = Client()
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(name="Test", slug="test")
        self.device_type = DeviceType.objects.create(slug="test", model="test", manufacturer=self.manufacturer)
        self.outlets = PowerOutletTemplate.objects.create(device_type=self.device_type, name="1")
        self.pduconfig = PDUConfig.objects.create(
            device_type=self.device_type, power_usage_oid="1.2.3.4", power_usage_unit="watts"
        )

        self.url = reverse("plugins:axians_netbox_pdu:pduconfig_edit", kwargs={"pk": self.pduconfig.pk})

    @override_settings(EXEMPT_VIEW_PERMISSIONS=["*"])
    def test_get_edit_anonymous(self):
        """Verify that the view cannot be accessed by anonymous users even if permissions are exempted."""
        self.client.logout()
        response = self.client.get(self.url)
        # Redirected to the login page
        self.assertEqual(response.status_code, 302)

    @override_settings(EXEMPT_VIEW_PERMISSIONS=[])
    def test_edit_get(self):
        """Verify that the view can be seen by a user with appropriate permissions."""
        # Attempt to access without permissions
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

        # Add permission
        self.user.user_permissions.add(
            Permission.objects.get(content_type__app_label="axians_netbox_pdu", codename="change_pduconfig")
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "axians_netbox_pdu/pduconfig_edit.html")

    @override_settings(EXEMPT_VIEW_PERMISSIONS=["*"])
    def test_post_edit_anonymous(self):
        """Verify that the view cannot be accessed by anonymous users even if permissions are exempted."""
        self.client.logout()
        response = self.client.get(self.url)
        # Redirected to the login page
        self.assertEqual(response.status_code, 302)

    @override_settings(EXEMPT_VIEW_PERMISSIONS=[])
    def test_edit_post(self):
        """Verify that the view can be used by a user with appropriate permissions."""
        # Attempt to access without permissions
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

        # Add permission
        self.user.user_permissions.add(
            Permission.objects.get(content_type__app_label="axians_netbox_pdu", codename="change_pduconfig")
        )

        self.device_type_1 = DeviceType.objects.create(slug="test1", model="test1", manufacturer=self.manufacturer)
        self.outlets_1 = PowerOutletTemplate.objects.create(device_type=self.device_type_1, name="1")

        response = self.client.post(
            self.url,
            data={"device_type": self.device_type_1.slug, "power_usage_oid": "5.5.5.5", "power_usage_unit": "watts"},
        )

        self.pduconfig.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PDUConfig.objects.count(), 1)
        self.assertEqual(self.pduconfig.power_usage_oid, "5.5.5.5")


class PDUConfigBulkDeleteViewTestCase(TestCase):
    """Test the PDUConfigBulkDeleteView view."""

    def setUp(self):
        """Create a user and baseline data for testing."""
        self.user = User.objects.create(username="testuser")
        self.client = Client()
        self.client.force_login(self.user)

        self.url = reverse("plugins:axians_netbox_pdu:pduconfig_bulk_delete")

        self.manufacturer = Manufacturer.objects.create(name="Test", slug="test")
        self.device_type = DeviceType.objects.create(slug="test", model="test", manufacturer=self.manufacturer)
        self.device_type_1 = DeviceType.objects.create(slug="test1", model="test1", manufacturer=self.manufacturer)
        self.outlets = PowerOutletTemplate.objects.create(device_type=self.device_type, name="1")
        self.outlets_1 = PowerOutletTemplate.objects.create(device_type=self.device_type_1, name="1")
        self.pduconfig_1 = PDUConfig.objects.create(
            device_type=self.device_type, power_usage_oid="1.1.1.1", power_usage_unit="watts"
        )
        self.pduconfig_2 = PDUConfig.objects.create(
            device_type=self.device_type_1, power_usage_oid="0.1.2.3", power_usage_unit="kilowatts"
        )

    @override_settings(EXEsMPT_VIEW_PERMISSIONS=["*"])
    def test_post_anonymous(self):
        """Verify that the view cannot be accessed by anonymous users even if permissions are exempted."""
        self.client.logout()
        response = self.client.post(self.url)
        # Redirected to the login page
        self.assertEqual(response.status_code, 302)

    @override_settings(EXEMPT_VIEW_PERMISSIONS=[])
    def test_post(self):
        """Verify that the view can be seen by a user with appropriate permissions."""
        # Attempt to access without permissions
        response = self.client.post(self.url, data={"pk": [self.pduconfig_1.pk], "confirm": True, "_confirm": True})
        self.assertEqual(response.status_code, 403)

        # Add permission
        self.user.user_permissions.add(
            Permission.objects.get(content_type__app_label="axians_netbox_pdu", codename="delete_pduconfig")
        )

        response = self.client.post(self.url, data={"pk": [self.pduconfig_1.pk], "confirm": True, "_confirm": True})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PDUConfig.objects.count(), 1)


class PDUConfigFeedBulkImportViewTestCase(TestCase):
    """Test the PDUConfigImportView view."""

    def setUp(self):
        """Create a superuser and baseline data for testing."""
        self.user = User.objects.create(username="testuser")
        self.client = Client()
        self.client.force_login(self.user)

        self.url = reverse("plugins:axians_netbox_pdu:pduconfig_import")

        self.manufacturer = Manufacturer.objects.create(name="Test", slug="test")
        self.device_type = DeviceType.objects.create(slug="test", model="test", manufacturer=self.manufacturer)
        self.device_type_1 = DeviceType.objects.create(slug="test1", model="test1", manufacturer=self.manufacturer)
        self.outlets = PowerOutletTemplate.objects.create(device_type=self.device_type, name="1")
        self.outlets_1 = PowerOutletTemplate.objects.create(device_type=self.device_type_1, name="1")

    @override_settings(EXEMPT_VIEW_PERMISSIONS=["*"])
    def test_get_anonymous(self):
        """Verify that the import view cannot be seen by an anonymous user even if permissions are exempted."""
        self.client.logout()
        response = self.client.get(self.url)
        # Redirected to the login page
        self.assertEqual(response.status_code, 302)

    @override_settings(EXEMPT_VIEW_PERMISSIONS=[])
    def test_get(self):
        """Verify that the import view can be seen by a user with appropriate permissions."""
        # Attempt to access without permissions
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

        # Add permission
        self.user.user_permissions.add(
            Permission.objects.get(content_type__app_label="axians_netbox_pdu", codename="add_pduconfig")
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "utilities/obj_bulk_import.html")

    @override_settings(EXEMPT_VIEW_PERMISSIONS=[])
    def test_post(self):
        """Verify that tasks can be bulk-imported."""
        csv_data = ["device_type,power_usage_oid,power_usage_unit", "test,0.1.2.3,watts", "test1,1.2.3.4,watts"]

        # Attempt to access without permissions
        response = self.client.post(self.url, data={"csv": "\n".join(csv_data)})
        self.assertEqual(response.status_code, 403)

        # Add permission
        self.user.user_permissions.add(
            Permission.objects.get(content_type__app_label="axians_netbox_pdu", codename="add_pduconfig")
        )

        response = self.client.post(self.url, data={"csv": "\n".join(csv_data)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PDUConfig.objects.count(), len(csv_data) - 1)
