from boilerplate import Boilerplate
from laravel import LaravelBoilerplate
from node_express import NodeExpressBoilerplate


class BoilerplateFactory():
    @staticmethod
    def fromInput(type: str, path: str, name: str) -> Boilerplate:
        for cls in Boilerplate.__subclasses__():
            if cls.isOfType(type):
                return cls(path, name)
        raise ValueError
