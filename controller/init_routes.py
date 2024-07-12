from controller.router import Router
from routes.currency_routes import (
    handle_get_currencies,
    handle_get_currency,
    handle_post_currency,
)
from routes.exchange_routes import handle_get_exchange_rates


class RouteInitializer:
    def __init__(self, router: Router) -> None:
        self.router = router

    def init_routes(self) -> None:
        # Currency routes
        self.router.add_route("/currencies", "GET", handle_get_currencies)
        self.router.add_route("/currency/", "GET", handle_get_currency)
        self.router.add_route("/currencies", "POST", handle_post_currency)

        # Exchange routes
        self.router.add_route("/exchangeRates", "GET", handle_get_exchange_rates)
