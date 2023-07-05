"""
These types are not reflecting any database content but are for triggering
functionality in the frontend from within a :class`~story_graph.models.Graph`.

These types can be used within a Python :class:`~story_graph.models.ScriptCell`
as they are also available within the :class:`~stream.engine.Engine`.

The stream subscription makes it possible to yield the
"""

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
    """Displays plain text."""

    text: str


@strawberry.type
class Checkbox:
    """A classic ``<checkbox>`` whose state (``true``/``false``) will be
    saved **as a string** under ``key`` in a :class:`~stream.models.StreamVariable`.
    """

    key: str
    label: str
    checked: bool = False


@strawberry.type
class Input:
    """A classic ``<inptut>`` which will save its content
    under the ``key`` as a :class:`~stream.models.StreamVariable`."""

    key: str
    label: str = "Info"
    placeholder: str = "Please input"


@strawberry.type
class Button:
    """A button which can also trigger a set of functionality."""

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
        """Constructor for a OK button which will"""
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
        """Constructor for a cancel button which will simply close
        the dialog and set the :class:`~story_graph.models.StreamVariable` ``CANCEL`` to ``'true'``
        (but as a string!).
        """
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
    """Triggers a popup on the frontend of the listener."""

    title: str
    content: List[Content]  # type: ignore
    buttons: List[Button]
