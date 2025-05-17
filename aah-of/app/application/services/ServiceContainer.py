class ServiceContainer:
    def __init__(self):
        self._services = {}
        self._factories = {}

    def register(self, name: str, factory, *args, **kwargs):
        if name not in self._factories:
            # stocke une lambda qui sait instancier avec ses paramètres
            self._factories[name] = lambda: factory(*args, **kwargs)

    def resolve(self, name: str):
        if name not in self._services:
            if name not in self._factories:
                raise ValueError(f"Service '{name}' not registered")
            self._services[name] = self._factories[name]()  # instanciation
        return self._services[name]
