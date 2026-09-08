# A simple async event emitter for the API
class Event:
    def __init__(self):
        self._handlers: dict[str, list] = {}
        self.ready = False # Set to True once the bot is ready.

    # Register a handler for an event
    def on(self, event: str):
        # Returns a decorator so it can be used with the @syntax
        def decorator(handler):
            self._handlers.setdefault(event, []).append(handler)
            return handler

        return decorator

    # Emit an event, calls all registered handlers with 'data'
    async def dispatch(self, event: str, data: Any = None):
        for handler in self._handlers[event]:
            await handler(data)