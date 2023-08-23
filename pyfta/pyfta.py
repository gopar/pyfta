import inspect
from typing import Any
from typing import Tuple
from typing import Generic
from typing import Callable
from typing import get_type_hints

from .randgen import RandomBase
from .randgen import RandomGenerator
from .containers import ContainerBase
from .exceptions import NoTypeAnnotationsFound

BUILTIN_TYPES = [int, bool, str, bytes, bytearray, float, complex, set, frozenset]
BUILTIN_CONTAINERS = [list, set, dict, frozenset]


def get_defaults(func: Callable) -> dict:
    """
    Return parameter and keyword defaults
    """
    signature = inspect.signature(func)
    parameters = signature.parameters

    defaults = {}
    for param_name, param in parameters.items():
        if param.default is not inspect.Parameter.empty:
            defaults[param_name] = param.default

    return defaults


def get_types_and_defaults(func: Callable, klass: Any = None) -> Tuple[dict, dict]:
    """Return the type annontations for given function/method and any defaults to use for calling that function/method.
    If a class is passed, it will look inside that class if there are any defined arguments.

    Will use default argument values if they exist, unless user has defined custom attributes to use, eg:

    class Pizza:
        def __init__(self, price: float, topping: str='meat', ):
            self.topping = topping

    class PizzaFactory(Pyfta):
       class Meta:
            model = Pizza

       topping = 'Ham'

    assert PizzaFactory().topping == 'Ham'
    assert PizzaFactory().price'
    """
    # TODO(Gopar): Handle case of metadata passing (eg typing.Annotated)
    type_signatures = get_type_hints(func, include_extras=True)
    defaults = get_defaults(func)

    if not klass:
        return (type_signatures, defaults)

    for name, value in type_signatures.items():
        attr = getattr(klass, name, None)

        if not attr:
            continue

        if isinstance(attr, RandomBase):
            defaults[name] = attr.generate()
        else:
            defaults[name] = attr
    return (type_signatures, defaults)


class PyftaMetaClass(type):
    INSTANCES_TO_CREATE = 3

    def __call__(cls) -> None:
        model = cls.Meta.model  # type: ignore
        type_signatures, defaults = get_types_and_defaults(model.__init__, cls)
        kwargs = get_params(
            type_signatures,
            defaults,
        )
        return model(**kwargs)


def get_params(type_signatures: dict, defaults: dict = {}) -> dict:
    """
    Return a dictionary that is ready to be passed into the callable as the **kwargs
    (Kwargs will explicitly have all arguments including the non-keyword ones)
    """
    if not type_signatures:
        raise NoTypeAnnotationsFound("Can only work with type annotated classes")

    if "return" in type_signatures:
        del type_signatures["return"]

    keywords = {}
    for name, signature in type_signatures.items():
        # Always use defaults first
        if name in defaults:
            keywords[name] = defaults[name]
        else:
            keywords[name] = resolve_signature(signature)

    return keywords


def resolve_signature(signature):  # type: ignore
    if signature in BUILTIN_TYPES:
        return RandomGenerator.from_data_type(signature)

    elif signature in BUILTIN_CONTAINERS:
        container = ContainerBase(signature, 5)
        return container.resolve()

    # User defined class
    elif inspect.isclass(signature) and not isinstance(signature, (Generic,)):
        type_signatures, defaults = get_types_and_defaults(signature.__init__)
        kwargs = get_params(type_signatures, defaults)
        return signature(**kwargs)

    elif isinstance(signature, Generic):
        raise Exception("Not yet implemented")

    raise Exception("Not yet implemented")


Pyfta = PyftaMetaClass("Pyfta", tuple(), {})
