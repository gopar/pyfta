import random
from typing import Any
from typing import List

from .randgen import RandomGenerator


class ContainerBase:
    def __init__(self, data_type: Any, how_many_to_create: int, allowed_types: List=None) -> None:
        self.data_type = data_type
        self.how_many_to_create = how_many_to_create
        self.allowed_types = allowed_types

    def resolve(self) -> Any:
        data_types = {
            list: ContainerList
        }
        container = data_types[self.data_type]
        return container(self.how_many_to_create, self.allowed_types).resolve()


class ContainerList:
    def __init__(self, how_many_to_create: int, allowed_types: List=None) -> None:
        self.how_many_to_create = how_many_to_create
        self.allowed_types = allowed_types or [int, str, float, bool]

    def resolve(self) -> Any:
        values = []
        for _ in range(self.how_many_to_create):
            data_type = random.choice(self.allowed_types)
            value = RandomGenerator.from_data_type(data_type)
            values.append(value)
        return values
