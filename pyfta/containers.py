import random
from typing import Any
from typing import List

from .randgen import RandomBase
from .randgen import RandomList
from .randgen import RandomGenerator


class ContainerBase:
    def __init__(self, data_type: Any, how_many_to_create: int, allowed_types: List=None) -> None:
        self.data_type = data_type
        self.how_many_to_create = how_many_to_create
        self.allowed_types = allowed_types

    def resolve(self) -> Any:
        data_types = {
            list: RandomList
        }
        container = data_types[self.data_type]
        return container(self.how_many_to_create, self.allowed_types)
