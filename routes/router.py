class Router:
    def __init__(self):
        self.get_handlers = []
        self.post_handlers = []
        self.patch_handlers = []

    def get(self, path):
        def register_get_handler(handler):
            self.get_handlers.append((path, handler))
            return handler
        return register_get_handler

    def post(self, path):
        def register_post_handler(handler):
            self.post_handlers.append((path, handler))
            return handler
        return register_post_handler
    
    def patch(self, path):
        def register_patch_handler(handler):
            self.patch_handlers.append((path, handler))
            return handler
        return register_patch_handler

    def find_handler(self, method, path: str):
        if method == 'GET':
            handlers = self.get_handlers
        elif method == 'POST':
            handlers = self.post_handlers
        elif method == 'PATCH':
            handlers = self.patch_handlers
        else:
            return None, None

        for handler_path, handler in handlers:
            if path.startswith(handler_path):
                return handler, path[len(handler_path):].strip('/')
        return None, None

