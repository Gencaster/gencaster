from enum import Enum
from typing import List, Optional

import strawberry
import strawberry.django


@strawberry.enum
class ButtonType(Enum):
    DEFAULT = "default"
    PRIMARY = "primary"
    SUCCESS = "success"
    WARNING = "warning"
    INFO = "info"
    DANGER = "danger"


@strawberry.type
class Text:
    text: str


@strawberry.type
class Checkbox:
    key: str
    label: str
    checked: bool = False


@strawberry.type
class Input:
    key: str
    label: str = "Info"
    placeholder: str = "Please input"


@strawberry.type
class Button:
    text: str
    button_type: ButtonType = ButtonType.DEFAULT

    send_variables_on_click: bool = False
    # will be used as key and its value will be set to true
    send_variable_on_click: Optional[str] = None

    @classmethod
    def ok(
        cls,
        text: str = "OK",
        send_variables_on_click: bool = True,
        button_type=ButtonType.PRIMARY,
        send_variable_on_click: str = "OK",
        **kwargs
    ):
        return cls(
            text=text,
            send_variables_on_click=send_variables_on_click,
            button_type=button_type,
            send_variable_on_click=send_variable_on_click,
            **kwargs,
        )

    @classmethod
    def cancel(
        cls,
        text: str = "Cancel",
        button_type=ButtonType.WARNING,
        send_variable_on_click: str = "CANCEL",
        **kwargs
    ):
        return cls(
            text=text,
            button_type=button_type,
            send_variable_on_click=send_variable_on_click,
            **kwargs,
        )


# @todo use typing.union which is supported by upcoming strawberry version
Content = strawberry.union("Content", [Text, Input, Checkbox])


@strawberry.type
class Dialog:
    title: str
    content: List[Content]  # type: ignore
    buttons: List[Button]
