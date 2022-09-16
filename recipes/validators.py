from django.core.exceptions import ValidationError
from pint.errors import UndefinedUnitError
import pint

valid_unit_measurements = ['pounds', 'lbs', 'oz', 'gram', 'kg']


def validate_unit_of_measure(value):
    ureg = pint.UnitRegistry()
    try:
        single_unit = ureg[value]
    except UndefinedUnitError as e:
        raise ValidationError(f"'{value}' is not a valid unit of measurements")
    except:
        raise ValidationError(f"'{value}' is not valid")
    # if value not in valid_unit_measurements:
