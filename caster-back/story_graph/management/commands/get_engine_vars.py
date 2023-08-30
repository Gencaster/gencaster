import dataclasses
import enum
import inspect
import json
from typing import Any, Dict, List, Optional

from django.core.management.base import BaseCommand

from story_graph.engine import Engine


class CompletionType(str, enum.Enum):
    CLASS = "class"
    CONSTANT = "constant"
    ENUM = "enum"
    FUNCTION = "function"
    INTERFACE = "interface"
    KEYWORD = "keyword"
    METHOD = "method"
    NAMESPACE = "namespace"
    PROPERTY = "property"
    TEXT = "text"
    TYPE = "type"
    VARIABLE = "variable"


@dataclasses.dataclass
class Completion:
    # from https://codemirror.net/docs/ref/#autocomplete
    label: str
    display_label: Optional[str] = None
    detail: Optional[str] = None
    info: Optional[str] = None
    apply: Optional[str] = None
    type: Optional[CompletionType] = None
    boost: Optional[int] = None
    section: Optional[str] = None


class Command(BaseCommand):
    help = "Creates a codemirror JSON with all available variables within a script cell for the editor"

    @staticmethod
    def empty_method():
        pass

    async def fake_wait_for_stream_variable(
        self, name: str, timeout: float = 100.0, update_speed: float = 0.5
    ):
        pass

    async def fake_get_stream_variables(self):
        pass

    def additional_vars(self) -> Dict[str, Any]:
        # fake some runtime vars via a similar type
        # like callable/var/etc
        return {
            "loop": Command.empty_method,
            "vars": {},
            "self": Engine,
            "get_stream_variables": self.fake_get_stream_variables,
            "wait_for_stream_variable": self.fake_wait_for_stream_variable,
        }

    def handle(self, *args, **options):
        vars = Engine.get_engine_global_vars()["__builtins__"]
        scoped_vars = {**vars, **self.additional_vars()}

        j: List[Completion] = []
        for k, v in scoped_vars.items():
            if callable(v):
                try:
                    j.append(
                        Completion(
                            label=k,
                            detail=str(inspect.signature(v)),
                            type=CompletionType.FUNCTION,
                            info=inspect.getdoc(v),
                        )
                    )
                except ValueError:
                    # e.g. int identifies as class but is also
                    # a callable
                    j.append(
                        Completion(
                            label=k,
                            type=CompletionType.CLASS,
                        )
                    )
            elif inspect.ismodule(v):
                j.append(Completion(label=k, detail="", type=CompletionType.NAMESPACE))
            elif inspect.isclass(v):
                j.append(
                    Completion(
                        label=k, type=CompletionType.CLASS, info=inspect.getdoc(v)
                    )
                )
            else:
                j.append(Completion(label=k, type=CompletionType.VARIABLE))

        n = [dataclasses.asdict(x) for x in j]
        print(json.dumps(n, indent=4))
