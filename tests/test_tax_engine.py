import pytest
from src.tax_engine import apply_tax

def test_apply_tax_foreign():
    tax, net = apply_tax(1000, 800, 'Fuente extranjera (29.5%)')
    assert tax == 200 * 0.295
    assert net == 1000 - tax