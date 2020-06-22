from utilities.choices import ChoiceSet


class PDUUnitChoices(ChoiceSet):
    """Valid values for PDUConfig "unit"."""

    UNIT_WATTS = "watts"
    UNIT_KILOWATTS = "kilowatts"

    CHOICES = ((UNIT_WATTS, "Watts"),)

    TEMPLATE_CHOICES = (
        (UNIT_WATTS, "Watts"),
        (UNIT_KILOWATTS, "Kilowatts"),
    )
