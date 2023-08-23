from typing import Text

import pytest

from pyfta import Pyfta
from pyfta.pyfta import get_defaults

# from pyfta import RandomGenerator


# @pytest.mark.parametrize('data_type', [
#     int, float, str, bool, bytes, bytearray
# ])
# def test_get_correct_value_based_on_type(data_type):
#     random_value = RandomGenerator.from_data_type(data_type)
#     assert isinstance(random_value, data_type)


def test_basic_metaclass_instantiation():
    class Pizza:
        pass

    class PizzaPyfta(Pyfta):
        class Meta:
            model = Pizza

    Pizza()


def test_metaclass_instantiation_with_attributes():
    class Pizza:
        def __init__(self, topping: str):
            self.topping = topping

    class PizzaPyfta(Pyfta):
        class Meta:
            model = Pizza

    pizza = PizzaPyfta()
    assert pizza.topping


def test_get_defaults():
    def func_with_defaults(
        w: int,
        x: float,
        y: str,
        a: str = "hey",
        b: int = 90,
        c: float = 3.14,
    ):
        pass

    defaults = get_defaults(func_with_defaults)

    for attr, default in [("a", "hey"), ("b", 90), ("c", 3.14)]:
        assert defaults[attr] == default


def test_multiple_classes():
    class World:
        def __init__(self, c: float, d: Text) -> None:
            self.c = c
            self.d = d

    class Hello:
        def __init__(self, a: int, b: str, c: World) -> None:
            self.a = a
            self.b = b
            self.c = c

    class HelloFactory(Pyfta):
        class Meta:
            model = Hello

    hw = HelloFactory()
