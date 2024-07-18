from sqlite3 import IntegrityError

from database.db_manager import connection_maker
from database.repo.currency import CurrencyRepo
from database.repo.exchange import ExchangeRepo
from database.transaction_manager import TransactionManager
from routes.router import Router

router = Router()


@router.get("/currencies")
def get_currencies() -> dict:
    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            repo = CurrencyRepo(cursor)
            currencies = repo.get_all_currencies()
    response = currencies.to_json()
    return {"status_code": 200, "body": response}


@router.get("/currency/")
def get_currency(code = None) -> dict:
    if not code:
        return {"status_code": 400, "body": "Currency code is required"}

    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            repo = CurrencyRepo(cursor)
            currency = repo.get_currency_by_code(code)
    if not currency:
        return {"status_code": 404, "body": "Currency not found"}
    response = currency.to_json()
    return {"status_code": 200, "body": response}


@router.get("/exchangeRates")
def handle_get_exchange_rates() -> dict:
    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            repo = ExchangeRepo(cursor)
            exchange_rates = repo.get_all_exchanges()
    response = exchange_rates.to_json()
    return {"status_code": 200, "body": response}


@router.get("/exchangeRate/")
def handle_get_exchange_rate(pair = None):
    if not pair:
        return {"status_code": 400, "body": "Currency pair is required"}
    
    base_currency_code = pair[:3]
    target_currency_code = pair[3:]
    
    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            currency_repo = CurrencyRepo(cursor)
            base_currency = currency_repo.get_currency_by_code(base_currency_code)
            target_currency = currency_repo.get_currency_by_code(target_currency_code)
         
            if not base_currency or not target_currency:
                return {"status_code": 404, "body": "Currency not found"}

            exchange_repo = ExchangeRepo(cursor)
            exchange_rate = exchange_repo.get_exchange_by_pair(base_currency, target_currency)

    if not exchange_rate:
        return {"status_code": 404, "body": "Exchange rate not found"}
    
    response = exchange_rate.to_json()
    return {"status_code": 200, "body": response}


@router.post("/currencies")
def handle_post_currency(form_data: dict):
    code = form_data.get("code")
    name = form_data.get("name")
    sign = form_data.get("sign") 
    
    if not code or not name or not sign:
        return {"status_code": 400, "body": "Currency code, name and sign are required"}

    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            repo = CurrencyRepo(cursor)
            try:
                currency = repo.add_currency(code, name, sign)
            except IntegrityError:
                return {"status_code": 409, "body": "Currency code already exists"}
    response = currency.to_json()
    return {"status_code": 201, "body": response}



@router.post('/exchangeRates')
def handle_post_exchange_rates(form_data: dict):
    print(form_data)
    base_currency_code = form_data.get("baseCurrencyCode")
    target_currency_code = form_data.get("targetCurrencyCode")
    rate = form_data.get("rate")
    
    if not base_currency_code or not target_currency_code or not rate:
        return {"status_code": 400, "body": "Currency codes and rate are required"}
    
    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            exchange_repo = ExchangeRepo(cursor)
            currency_repo = CurrencyRepo(cursor)
            
            base_currency = currency_repo.get_currency_by_code(base_currency_code)
            target_currency = currency_repo.get_currency_by_code(target_currency_code)
            
            if not base_currency or not target_currency:
                return {"status_code": 404, "body": "Currency not found"}
            
            try: 
                exchange_rate = exchange_repo.add_exchange(base_currency, target_currency, rate)
            except IntegrityError:
                return {"status_code": 409, "body": "Exchange rate already exists"}
    
    response = exchange_rate.to_json()
    return {"status_code": 201, "body": response} 




@router.patch("/exchangeRate/")
def handle_patch_exchange_rates(form_data: dict, pair = None):
    rate = form_data.get("rate")

    if not rate:
        return {"status_code": 400, "body": "Rate is required"}
    
    if not pair:
        return {"status_code": 400, "body": "Currency pair is required"}
    
    base_currency_code = pair[:3]
    target_currency_code = pair[3:]
    
    with connection_maker() as conn:
        with TransactionManager(conn) as cursor:
            currency_repo = CurrencyRepo(cursor)
            base_currency = currency_repo.get_currency_by_code(base_currency_code)
            target_currency = currency_repo.get_currency_by_code(target_currency_code)
            
            if not base_currency or not target_currency:
                return {"status_code": 404, "body": "Currency not found"}
            
            exchange_repo = ExchangeRepo(cursor)
            exchange_rate = exchange_repo.get_exchange_by_pair(base_currency, target_currency)
            
            if not exchange_rate:
                return {"status_code": 404, "body": "Exchange rate not found"}
            
            exchange_rate = exchange_repo.update_exchange(exchange_rate, rate)
        
    response = exchange_rate.to_json()
    return {"status_code": 200, "body": response}
        