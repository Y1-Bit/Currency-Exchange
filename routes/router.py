from typing import Callable


class Router:
    def __init__(self):
        self.get_handlers: list[tuple[str, Callable]] = []
        self.post_handlers: list[tuple[str, Callable]] = []
        self.patch_handlers: list[tuple[str, Callable]] = []

    def get(self, path: str) -> Callable:
        def register_get_handler(handler: Callable) -> Callable:
            self.get_handlers.append((path, handler))
            return handler

        return register_get_handler

    def post(self, path: str) -> Callable:
        def register_post_handler(handler: Callable) -> Callable:
            self.post_handlers.append((path, handler))
            return handler

        return register_post_handler

    def patch(self, path: str) -> Callable:
        def register_patch_handler(handler: Callable) -> Callable:
            self.patch_handlers.append((path, handler))
            return handler

        return register_patch_handler

    def find_handler(
        self, method: str, path: str
    ) -> tuple[Callable | None, str | None]:
        if method == "GET":
            handlers = self.get_handlers
        elif method == "POST":
            handlers = self.post_handlers
        elif method == "PATCH":
            handlers = self.patch_handlers
        else:
            return None, None

        for handler_path, handler in handlers:
            if path.startswith(handler_path):
                return handler, path[len(handler_path) :].strip("/")
        return None, None
