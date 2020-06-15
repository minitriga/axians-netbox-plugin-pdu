from utilities.choices import ChoiceSet


class PDUUnitChoices(ChoiceSet):
    """Valid values for PDUConfig "unit"."""

    UNIT_WATTS = "watts"
    UNIT_KILOWATTS = "kilowatts"

    CHOICES = (
        (UNIT_WATTS, "watts"),
        (UNIT_KILOWATTS, "kilowatts"),
    )
