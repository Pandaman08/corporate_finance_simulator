def convert_tea_to_periodic(tea, m):
    return (1 + tea) ** (1 / m) - 1

def validate_inputs(**kwargs):
    errors = []
    if kwargs.get('initial_amount', 0) < 0:
        errors.append("Monto inicial no puede ser negativo.")
    if kwargs.get('periodic_contribution', 0) < 0:
        errors.append("Aporte periódico no puede ser negativo.")
    if kwargs.get('tea', -1) < 0 or kwargs.get('tea', 0) > 50:
        errors.append("TEA debe estar entre 0% y 50%.")
    if kwargs.get('years', 0) <= 0:
        errors.append("El plazo debe ser mayor a cero.")
    if kwargs.get('face_value', 0) < 0:
        errors.append("Valor nominal no puede ser negativo.")
    if kwargs.get('coupon_rate', -1) < 0:
        errors.append("Tasa cupón no puede ser negativa.")
    if kwargs.get('required_yield', -1) < 0:
        errors.append("Tasa de retorno esperada no puede ser negativa.")
    return errors