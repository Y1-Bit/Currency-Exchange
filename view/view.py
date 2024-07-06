import json
from model.model import Currency

def show_currencies(currencies: list[Currency]) -> str:
    return json.dumps([{
        "id": currency.id,
        "code": currency.code,
        "full_name": currency.full_name,
        "sign": currency.sign
    } for currency in currencies])