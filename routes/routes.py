from routes.router import Router
from services.currency import *
from services.exchange import *
from exceptions import (
    CurrencyNotFoundException,
    ExchangeRateNotFoundException,
    CurrencyAlreadyExistsException,
    ExchangeAlreadyExistsException,
)

router = Router()


@router.get("/currencies")
def get_currencies() -> dict:
    currency_list = get_all_currencies()
    response = currency_list.to_json()
    return {"status_code": 200, "body": response}


@router.get("/currency/")
def get_currency(code: str | None = None) -> dict:
    if not code:
        return {"status_code": 400, "body": "Currency code is required"}
    try:
        currency = get_currency_by_code(code)
    except CurrencyNotFoundException:
        return {"status_code": 404, "body": "Currency not found"}

    response = currency.to_json()
    return {"status_code": 200, "body": response}


@router.get("/exchangeRates")
def handle_get_exchange_rates() -> dict:
    exchange_list = get_all_exchange_rates()
    response = exchange_list.to_json()
    return {"status_code": 200, "body": response}


@router.get("/exchangeRate/")
def handle_get_exchange_rate(query: dict) -> dict:
    pair = query.get("pair")
    if not pair:
        return {"status_code": 400, "body": "Currency pair is required"}
    try:
        exchange = get_exchange_rate_by_pair(pair)
    except ExchangeRateNotFoundException:
        return {"status_code": 404, "body": "Exchange rate not found"}

    response = exchange.to_json()
    return {"status_code": 200, "body": response}


@router.post("/currencies")
def handle_post_currency(form_data: dict) -> dict:
    code = form_data.get("code")
    name = form_data.get("name")
    sign = form_data.get("sign")

    if not code or not name or not sign:
        return {
            "status_code": 400,
            "body": "Currency code, name and sign are required",
        }

    try:
        currency = add_currency(code, name, sign)
    except CurrencyAlreadyExistsException:
        return {"status_code": 409, "body": "Currency already exists"}
    except CurrencyNotFoundException:
        return {"status_code": 404, "body": "Currency not found"}

    response = currency.to_json()
    return {"status_code": 201, "body": response}

@router.post("/exchangeRates")
def handle_post_exchange_rates(form_data: dict) -> dict:
    base_currency_code = form_data.get("baseCurrencyCode")
    target_currency_code = form_data.get("targetCurrencyCode")
    rate = form_data.get("rate")

    if not base_currency_code or not target_currency_code or not rate:
        return {"status_code": 400, "body": "Currency codes and rate are required"}

    try:
        exchange = add_exchange_rate(base_currency_code, target_currency_code, rate)
    except CurrencyNotFoundException:
        return {"status_code": 404, "body": "Currency not found"}
    except ExchangeAlreadyExistsException:
        return {"status_code": 409, "body": "Exchange already exists"}

    response = exchange.to_json()
    return {"status_code": 201, "body": response}

@router.patch("/exchangeRate/")
def handle_patch_exchange_rates(form_data: dict, pair: str | None = None) -> dict:
    rate = form_data.get("rate")

    if not rate:
        return {"status_code": 400, "body": "Rate is required"}

    if not pair:
        return {"status_code": 400, "body": "Currency pair is required"}

    base_currency_code = pair[:3]
    target_currency_code = pair[3:]

    try:
        exchange = update_exchange_rate(base_currency_code, target_currency_code, rate)
    except CurrencyNotFoundException:
        return {"status_code": 404, "body": "Currency not found"}

    response = exchange.to_json()
    return {"status_code": 200, "body": response}

@router.get("/exchange")
def handle_get_exchange(query: dict) -> dict:
    base_currency_code = query.get("from")
    target_currency_code = query.get("to")
    amount = query.get("amount")

    if not base_currency_code or not target_currency_code:
        return {"status_code": 400, "body": "Currency codes are required"}

    if not amount:
        return {"status_code": 400, "body": "Amount is required"}

    base_currency_code = base_currency_code[0]
    target_currency_code = target_currency_code[0]
    amount = amount[0]

    try:
        exchange_result = get_exchange(base_currency_code, target_currency_code, amount)
    except CurrencyNotFoundException:
        return {"status_code": 404, "body": "Currency not found"}
    except ExchangeRateNotFoundException:
        return {"status_code": 404, "body": "Exchange rate not found"}

    response = exchange_result.to_json()
    return {"status_code": 200, "body": response}