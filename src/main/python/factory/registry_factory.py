from typing import ClassVar, Any, Callable, Type


class BaseInterface:  # Abstract Base Class
    def __init__(self) -> None:
        raise NotImplementedError("Cannot create instance of an abstract class")

    def getName(self) -> str:  # Abstract method
        raise NotImplementedError("Must implement 'getName' in subclasses")


class RegistryFactory:
    """A registry to manage and retrieve instances of BaseInterface."""

    _registry: ClassVar[dict[str, Callable[[], BaseInterface]]] = {}

    @staticmethod
    def add(name: str, proc: Callable[[], BaseInterface]) -> None:
        """Add a new factory method to the registry."""
        RegistryFactory._registry[name] = proc

    @staticmethod
    def getInstance(name: str) -> BaseInterface:
        """Retrieve an instance of a registered class by name."""
        init = RegistryFactory._registry.get(name)
        if init:
            return init()
        raise KeyError(f"Class '{name}' is not registered in the factory.")


class First(BaseInterface):
    def __init__(self) -> None:
        pass

    def getName(self) -> str:
        return "first"


if __name__ == "__main__":
    # Register the 'First' class in the factory
    RegistryFactory.add("first", First)

    # Retrieve an instance of 'First' using the factory
    first_instance = RegistryFactory.getInstance("first")
    print(first_instance.getName())  # Output: "first"
