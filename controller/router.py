class Router:
    def __init__(self):
        self.get_handlers = []
        self.post_handlers = []

    def get(self, path):
        def register_get_handler(handler):
            self.get_handlers.append((path, handler))
            print(self.get_handlers)
            return handler
        return register_get_handler

    def post(self, path):
        def register_post_handler(handler):
            self.post_handlers.append((path, handler))
            return handler
        return register_post_handler

    def find_handler(self, method, path):
        handlers = self.get_handlers if method == 'GET' else self.post_handlers
        for handler_path, handler in handlers:
            if handler_path in path:
                return handler
        return None

router = Router()
