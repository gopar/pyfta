import abc
import random
from string import ascii_letters
from typing import Any
from typing import List


class RandomBase(abc.ABC):
    @abc.abstractmethod
    def generate(self) -> Any:
        raise NotImplementedError()


class RandomString(RandomBase):
    SIGNATURE = str

    def __init__(self, chars: str=ascii_letters, prefix: str='', suffix: str='', length: int=10) -> None:
        self.chars = chars
        self.prefix = prefix
        self.suffix = suffix
        self.length = length

    def generate(self) -> str:
        string = ''.join(random.choices(ascii_letters, k=self.length))
        return self.prefix + string + self.suffix


class RandomInt(RandomBase):
    SIGNATURE = int

    def __init__(self, lower_limit: int=0, upper_limit: int=100) -> None:
        self.lower = lower_limit
        self.upper = upper_limit

    def generate(self) -> int:
        number = random.randint(self.lower, self.upper)
        return number


class RandomFloat(RandomBase):
    SIGNATURE = float

    def __init__(self, lower_limit: int=0, upper_limit: int=99) -> None:
        self.lower = lower_limit
        self.upper = upper_limit

    def generate(self) -> float:
        decimal = random.random()
        number = random.randint(self.lower, self.upper)
        return number + decimal


class RandomBool(RandomBase):
    SIGNATURE = bool

    def generate(self) -> bool:
        return True if random.randint(0, 1) else False


class RandomGenerator:
    def __init__(self, data_type: Any, **kwargs: dict) -> None:
        self.data_type = data_type

    @classmethod
    def from_data_type(cls: Any, data_type: Any) -> RandomBase:
        data_types = {
            int: RandomInt,
            str: RandomString,
            float: RandomFloat,
            bool: RandomBool
        }
        return data_types[data_type]().generate()


class RandomList(RandomBase):
    def __init__(self, how_many_to_create: int, allowed_types: List=None) -> None:
        self.how_many_to_create = how_many_to_create
        self.allowed_types = allowed_types or [int, str, float, bool]

    def generate(self) -> Any:
        values = []
        for _ in range(self.how_many_to_create):
            data_type = random.choice(self.allowed_types)
            value = RandomGenerator.from_data_type(data_type)
            values.append(value)
        return values
