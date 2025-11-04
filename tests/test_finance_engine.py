import pytest
import pandas as pd
from src.finance_engine import calculate_portfolio_growth, calculate_monthly_pension, bond_present_value

def test_calculate_portfolio_growth():
    df, final = calculate_portfolio_growth(1000, 100, 'Anual', 1, 10)
    assert len(df) == 2
    assert final > 1000

def test_calculate_monthly_pension():
    pension = calculate_monthly_pension(100000, 20, 4)
    assert pension > 0

def test_bond_present_value():
    df, pv = bond_present_value(1000, 5, 'Anual', 5, 6)
    assert pv > 0
    assert len(df) == 5