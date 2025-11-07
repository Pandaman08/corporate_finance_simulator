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
    required_yield,
    use_tea=True
):
    """
    Calcula el valor presente de un bono con detalle completo por periodo.
    
    Args:
        face_value: Valor nominal del bono
        coupon_rate: Tasa del cupón (% anual)
        payment_freq: Frecuencia de pago ('Mensual', 'Bimestral', etc.)
        years_to_maturity: Años hasta el vencimiento
        required_yield: Tasa de retorno requerida (% anual)
        use_tea: Si True, usa TEA; si False, usa tasa nominal
    
    Returns:
        df: DataFrame con detalle de flujos por periodo
        pv_total: Valor presente total del bono
        summary: Diccionario con información resumen
    """
    # Validaciones de entrada
    if coupon_rate < 0 or coupon_rate > 100:
        raise ValueError("La tasa cupón debe estar entre 0 y 100%")
    
    freq_map = {
        'Mensual': 12,
        'Bimestral': 6,
        'Trimestral': 4,
        'Cuatrimestral': 3,
        'Semestral': 2,
        'Anual': 1
    }
    
    if payment_freq not in freq_map:
        raise ValueError(f"Frecuencia no válida. Opciones: {list(freq_map.keys())}")
    
    periods_per_year = freq_map[payment_freq]
    total_periods = int(years_to_maturity * periods_per_year)
    
    if total_periods == 0:
        raise ValueError("El plazo debe generar al menos un periodo de pago")
    
    # Cálculo de la tasa periódica y cupón
    if use_tea:
        # Para el cupón: usar tasa nominal simple (estándar en bonos)
        coupon_periodic_rate = (coupon_rate / 100) / periods_per_year
        # Para descuento: convertir TEA a tasa periódica efectiva
        discount_rate = convert_tea_to_periodic(required_yield / 100, periods_per_year)
    else:
        # Tasa nominal simple para ambos
        coupon_periodic_rate = (coupon_rate / 100) / periods_per_year
        discount_rate = (required_yield / 100) / periods_per_year
    
    coupon_payment = face_value * coupon_periodic_rate
    
    # Construcción de tabla de flujos con detalle completo
    periodos = []
    flujos_cupon = []
    flujos_principal = []
    flujos_totales = []
    factores_descuento = []
    valores_presentes = []
    
    for t in range(1, total_periods + 1):
        # Flujos
        cupon = coupon_payment
        principal = face_value if t == total_periods else 0.0
        flujo_total = cupon + principal
        
        # Factor de descuento
        factor = 1 / ((1 + discount_rate) ** t)
        
        # Valor presente
        vp = flujo_total * factor
        
        periodos.append(t)
        flujos_cupon.append(round(cupon, 2))
        flujos_principal.append(round(principal, 2))
        flujos_totales.append(round(flujo_total, 2))
        factores_descuento.append(round(factor, 6))
        valores_presentes.append(round(vp, 2))

    df = pd.DataFrame({
        'Periodo': periodos,
        'Cupón': flujos_cupon,
        'Principal': flujos_principal,
        'Flujo Total': flujos_totales,
        'Factor Descuento': factores_descuento,
        'Valor Presente': valores_presentes
    })
    
    # Valor presente total (redondeado)
    pv_total = round(sum(valores_presentes), 2)
    
    total_cupones = round(sum(flujos_cupon), 2)
    vp_cupones = round(df['Valor Presente'].iloc[:-1].sum(), 2) if total_periods > 1 else 0
    vp_principal = round(df['Valor Presente'].iloc[-1], 2)
    
    summary = {
        'total_periods': total_periods,
        'coupon_payment': round(coupon_payment, 2),
        'total_coupons': total_cupones,
        'vp_coupons': vp_cupones,
        'vp_principal': vp_principal,
        'discount_rate_periodic': round(discount_rate * 100, 4),
        'premium_discount': round(pv_total - face_value, 2),
        'premium_discount_pct': round(((pv_total / face_value) - 1) * 100, 2)
    }
    
    return df, pv_total, summary