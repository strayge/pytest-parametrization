from collections import namedtuple
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)

import pytest
import six

__all__ = [
    'Parametrization'
]


class Parametrization:
    def __init__(self, test_function: Callable[..., Any]) -> None:
        self.test_function: Callable[..., Any] = test_function

        self.name_factory_func: Optional[Callable[..., str]] = None
        self.cases: List[Tuple[Optional[str], Any, Any]] = []
        self.defaults: Dict[str, Any] = {}

    def get_decorated(self, parameters: Optional[Iterable[str]] = None) -> Any:
        if parameters is None:
            parameters_set: Set[str] = set()
            for case in self.cases:
                name, args, kwargs = case
                if args:
                    raise Exception(
                        "args are forbidden with auto-detection, "
                        "please use kwargs"
                    )
                parameters_set.update(six.viewkeys(kwargs))
            parameters_set.update(six.viewkeys(self.defaults))
            parameters = parameters_set

        arguments_names = list(parameters)

        arguments_values: List[Tuple] = []
        ids: List[str] = []

        case_cls = namedtuple('Case', arguments_names)  # type: ignore

        for name, args, kwargs in reversed(self.cases):
            for argument_name in arguments_names[len(args):]:
                if (
                    argument_name not in kwargs
                    and argument_name in self.defaults
                ):
                    kwargs[argument_name] = self.defaults[argument_name]

            if name is None:
                assert self.name_factory_func, (
                    'Name factory must be given '
                    'with @Parametrization.name_factory'
                )
                name = self.name_factory_func(**kwargs)

            ids.append(name)

            arguments_values.append(tuple(case_cls(*args, **kwargs)))

        return pytest.mark.parametrize(
            argnames=arguments_names,
            argvalues=arguments_values,
            ids=ids,
        )(self.test_function)

    def add_case(self, name: Optional[str], *args: Any, **kwargs: Any) -> None:
        self.cases.append((name, args, kwargs))

    def add_legacy_cases(
        self, base_name: str, fields: Iterable[str], values: Iterable[Any],
    ) -> None:
        fields_with_values = [dict(zip(fields, value)) for value in values]
        for case in fields_with_values:
            name = "{} -> {}".format(
                base_name,
                ", ".join([
                    '='.join([str(v) for v in case_values])
                    for case_values in case
                ])
            )
            self.add_case(name, **case)

    @classmethod
    def parameters(cls, *parameters: str) -> Callable[..., Any]:
        def decorator(f: Union[Callable[..., Any], 'Parametrization']) -> Any:
            if not isinstance(f, Parametrization):
                return Parametrization(f).get_decorated(parameters)
            return f.get_decorated(parameters)

        return decorator

    @classmethod
    def autodetect_parameters(cls) -> Callable[..., Any]:
        def decorator(f: Union[Callable, 'Parametrization']) -> Any:
            if not isinstance(f, Parametrization):
                return Parametrization(f).get_decorated()
            return f.get_decorated()

        return decorator

    @classmethod
    def name_factory(cls, create_name: Any) -> Callable:
        def decorator(f: Union[Callable, 'Parametrization']) -> Any:
            if not isinstance(f, Parametrization):
                parametrization = Parametrization(f)
            else:
                parametrization = f
            parametrization.name_factory_func = create_name

            return parametrization

        return decorator

    @classmethod
    def case(
        cls, name: Optional[str] = None, *args: Any, **kwargs: Any
    ) -> Callable:
        def decorator(f: Union[Callable, 'Parametrization']) -> Any:
            if not isinstance(f, Parametrization):
                parametrization = Parametrization(f)
            else:
                parametrization = f
            parametrization.add_case(name, *args, **kwargs)

            return parametrization

        return decorator

    @classmethod
    def default_parameters(cls, **kwargs: Any) -> Callable:
        def decorator(f: Union[Callable, 'Parametrization']) -> Any:
            if not isinstance(f, Parametrization):
                parametrization = Parametrization(f)
            else:
                parametrization = f

            for key, value in six.iteritems(kwargs):
                parametrization.defaults[key] = value

            return parametrization

        return decorator

    @classmethod
    def legacy_cases(
        cls, base_name: str, fields: Iterable[str], values: Iterable[Any]
    ) -> Callable:
        def decorator(f: Union[Callable, 'Parametrization']) -> Any:
            if not isinstance(f, Parametrization):
                parametrization = Parametrization(f)
            else:
                parametrization = f
            parametrization.add_legacy_cases(base_name, fields, values)

            return parametrization

        return decorator
