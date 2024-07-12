class Router:
    def __init__(self) -> None:
        self.routes = {}

    def add_route(self, path, method, handler) -> None:
        self.routes[(path, method)] = handler

    def get_handler(self, path, method):
        return self.routes.get((path, method))