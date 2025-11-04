def apply_tax(gross_amount, initial_amount, tax_type):
    gain = max(0.0, gross_amount - initial_amount)
    if tax_type == 'Fuente extranjera (29.5%)':
        tax = gain * 0.295
    elif tax_type == 'Bolsa local (5%)':
        tax = gain * 0.05
    else:
        tax = 0.0
    net_amount = gross_amount - tax
    return tax, net_amount