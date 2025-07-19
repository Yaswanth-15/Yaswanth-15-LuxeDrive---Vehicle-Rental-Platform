from decimal import Decimal

def Decimal2Float(value):
    return float(value) if isinstance(value, Decimal) else value