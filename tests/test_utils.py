import pytest
from src.utils import convert_tea_to_periodic, validate_inputs

def test_convert_tea_to_monthly():
    r = convert_tea_to_periodic(0.12, 12)
    assert abs((1 + r)**12 - 1.12) < 1e-10

def test_validate_negative_amount():
    errors = validate_inputs(initial_amount=-100)
    assert len(errors) == 1