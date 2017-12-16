import inspect
from typing import Any
from typing import GenericMeta
from typing import get_type_hints
from typing import _FinalTypingBase

from .randgen import RandomGenerator
from .container import ContainerBase
from .exceptions import NoTypeAnnotationsFound

BUILTIN_TYPES = [int, bool, str, bytes, bytearray, float, complex, set, frozenset]
BUILTIN_CONTAINERS = [list, set, dict, frozenset]


class PyftaMetaClass(type):
    def __call__(cls):
        model = cls.Meta.model
        type_signatures = get_type_hints(model.__init__)
        kwargs = get_params(type_signatures)
        return model(**kwargs)


def get_params(type_signatures: dict) -> dict:
    if not type_signatures:
        raise NoTypeAnnotationsFound('Can only work with type annotated classes')
    keywords = {}
    if 'return' in type_signatures:
        del type_signatures['return']
    for name, signature in type_signatures.items():
        keywords[name] = resolve_signature(signature)

    return keywords


def resolve_signature(signature):
    if signature in BUILTIN_TYPES:
        return RandomGenerator.from_data_type(signature)
    elif signature in BUILTIN_CONTAINERS:
        container = ContainerBase(signature, 5)
        return container.resolve()
    # User defined class
    elif inspect.isclass(signature) and not isinstance(signature, (GenericMeta, _FinalTypingBase)):
        params = get_params(get_type_hints(signature.__init__))
        return signature(**params)
    elif not signature.__args__ and isinstance(signature, GenericMeta):
        container = ContainerBase(signature.__extra__, 5)
        return container.resolve()
    elif isinstance(signature, GenericMeta):
        container = ContainerBase(signature.__extra__, 5, list(signature.__args__))
        return container.resolve()
    elif isinstance(signature, _FinalTypingBase):
        raise Exception('Not yet implemented')
    raise Exception('Not yet implemented')



Pyfta = PyftaMetaClass('Pyfta', tuple(), {})
# Pyfta.INSTANCES_TO_CREATE = 5
