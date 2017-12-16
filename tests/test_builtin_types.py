import pytest

from pyfta import Pyfta
from pyfta import RandomGenerator


@pytest.mark.parametrize('data_type', [
    int, float, str, bool, bytes, bytearray
])
def test_get_correct_value_based_on_type(data_type):
    random_value = RandomGenerator.from_data_type(data_type)
    assert isinstance(random_value, data_type)
