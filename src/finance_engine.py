import numpy as np
import pandas as pd
from .utils import convert_tea_to_periodic

def calculate_portfolio_growth(
    initial_amount,
    periodic_contribution,
    contribution_freq,
    years,
    tea
):
    periods_per_year = {
        'Mensual': 12,
        'Trimestral': 4,
        'Semestral': 2,
        'Anual': 1
    }[contribution_freq]
    
    r = convert_tea_to_periodic(tea / 100, periods_per_year)
    n_periods = int(years * periods_per_year)
    
    periods = []
    balance = initial_amount
    total_contributions = initial_amount
    for i in range(n_periods + 1):
        if i == 0:
            interest = 0.0
        else:
            interest = balance * r
            balance += interest
            if periodic_contribution > 0:
                balance += periodic_contribution
                total_contributions += periodic_contribution
        
        periods.append({
            'Periodo': i,
            'Aporte': periodic_contribution if i > 0 else initial_amount,
            'Saldo_Inicial': balance - interest - (periodic_contribution if i > 0 else 0),
            'Interes': interest,
            'Saldo_Final': balance
        })
    
    return pd.DataFrame(periods), balance

def calculate_monthly_pension(
    capital,
    retirement_years,
    tea_retirement
):
    if retirement_years <= 0 or tea_retirement <= 0:
        return 0.0
    r_monthly = convert_tea_to_periodic(tea_retirement / 100, 12)
    n_months = int(retirement_years * 12)
    if r_monthly == 0:
        return capital / n_months if n_months > 0 else 0.0
    pension = capital * (r_monthly / (1 - (1 + r_monthly) ** (-n_months)))
    return pension

def bond_present_value(
    face_value,
    coupon_rate,
    payment_freq,
    years_to_maturity,
    required_yield
):
    freq_map = {
        'Mensual': 12,
        'Bimestral': 6,
        'Trimestral': 4,
        'Cuatrimestral': 3,
        'Semestral': 2,
        'Anual': 1
    }
    periods_per_year = freq_map[payment_freq]
    coupon_payment = (coupon_rate / 100) * face_value / periods_per_year
    total_periods = int(years_to_maturity * periods_per_year)
    r = convert_tea_to_periodic(required_yield / 100, periods_per_year)
    
    cash_flows = []
    pv_flows = []
    for t in range(1, total_periods + 1):
        cf = coupon_payment
        if t == total_periods:
            cf += face_value
        pv = cf / ((1 + r) ** t)
        cash_flows.append(cf)
        pv_flows.append(pv)
    
    pv_total = sum(pv_flows)
    df = pd.DataFrame({
        'Periodo': range(1, total_periods + 1),
        'Flujo': cash_flows,
        'VP': pv_flows
    })
    return df, pv_total