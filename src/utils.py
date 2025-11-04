def convert_tea_to_periodic(tea, m):
    """Convierte una Tasa Efectiva Anual (tea) a tasa periódica con m períodos al año."""
    if m <= 0:
        raise ValueError("El número de períodos por año debe ser mayor a cero.")
    return (1 + tea) ** (1 / m) - 1

def validate_module_a(**kwargs):
    errors = []
    if kwargs.get('initial_amount', 0) < 0:
        errors.append("Monto inicial no puede ser negativo.")
    if kwargs.get('periodic_contribution', 0) < 0:
        errors.append("Aporte periódico no puede ser negativo.")
    if kwargs.get('tea', -1) < 0 or kwargs.get('tea', 0) > 50:
        errors.append("TEA debe estar entre 0% y 50%.")
    if kwargs.get('years', 0) <= 0:
        errors.append("El plazo debe ser mayor a cero.")
    return errors

def validate_module_b(**kwargs):
    errors = []
    if kwargs.get('tea_retirement', -1) < 0 or kwargs.get('tea_retirement', 0) > 50:
        errors.append("Tasa de retorno durante retiro debe estar entre 0% y 50%.")
    if kwargs.get('retirement_years', 0) <= 0:
        errors.append("Los años esperados de retiro deben ser mayores a cero.")
    return errors

def validate_module_c(**kwargs):
    errors = []
    if kwargs.get('face_value', 0) < 0:
        errors.append("Valor nominal no puede ser negativo.")
    if kwargs.get('coupon_rate', -1) < 0:
        errors.append("Tasa cupón no puede ser negativa.")
    if kwargs.get('required_yield', -1) < 0:
        errors.append("Tasa de retorno esperada no puede ser negativa.")
    if kwargs.get('years_to_maturity', 0) <= 0:
        errors.append("El plazo del bono debe ser mayor a cero.")
    return errors