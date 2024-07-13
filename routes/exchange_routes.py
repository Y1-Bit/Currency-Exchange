from controller import RequestHandler
from database.repo.requests import RequestsRepo


def handle_get_exchange_rates(handler: RequestHandler, query, repo: RequestsRepo) -> None:
    ...
