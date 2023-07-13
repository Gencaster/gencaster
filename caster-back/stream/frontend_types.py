"""
These types are not reflecting any database content but are for triggering
functionality in the frontend from within a :class`~story_graph.models.Graph`.

These types can be used within a Python :class:`~story_graph.models.ScriptCell`
as they are also available within the :class:`~stream.engine.Engine`.

The stream subscription makes it possible to yield the
"""

from dataclasses import field
from enum import Enum
from typing import List

import strawberry
import strawberry.django


@strawberry.enum
class ButtonType(Enum):
    """Derived from ElementPlus framework, see
    `https://element-plus.org/en-US/component/button.html`_."""

    DEFAULT = "default"
    PRIMARY = "primary"
    SUCCESS = "success"
    WARNING = "warning"
    INFO = "info"
    DANGER = "danger"


@strawberry.enum
class CallbackAction(Enum):
    """Allows to add a pre-defined JavaScript callback to a button or a checkbox.

    ACTIVATE_GPS_STREAMING          Activates streaming of GPS coordinates
                                    as :class:`~stream.models.StreamVariable`.
                                    If the GPS request succeeds the dialog will be closed,
                                    if not it the user will be forwarded to an error page
                                    which describes the setup procedure for the OS.
    SEND_VARIABLES                  Send all variables of the form / dialog to
                                    the server.
    SEND_VARIABLE                   Sends a single :class:`~stream.models.StreamVariable`
                                    with the key/value of the where the callback is
                                    attached to.
    """

    ACTIVATE_GPS_STREAMING = "activate_gps_streaming"
    SEND_VARIABLES = "send_variables"
    SEND_VARIABLE = "send_variable"


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
    callback_actions: List[CallbackAction] = field(default_factory=lambda: [])

    @classmethod
    def gps(
        cls, label: str = "Is it OK to access your GPS?", key: str = "gps", **kwargs
    ):
        return cls(
            label=label,
            key=key,
            callback_actions=[CallbackAction.ACTIVATE_GPS_STREAMING],
        )


@strawberry.type
class Input:
    """A classic ``<inptut>`` which will save its content
    under the ``key`` as a :class:`~stream.models.StreamVariable`."""

    key: str
    label: str = "input"
    placeholder: str = "Please input"


@strawberry.type
class Button:
    """A button which can also trigger a set of functionality."""

    text: str
    value: str
    key: str = "button"
    button_type: ButtonType = ButtonType.DEFAULT
    callback_actions: List[CallbackAction] = field(
        default_factory=lambda: [CallbackAction.SEND_VARIABLE]
    )

    @classmethod
    def ok(
        cls,
        text: str = "OK",
        value="ok",
        button_type=ButtonType.PRIMARY,
        callback_actions: List[CallbackAction] = [
            CallbackAction.SEND_VARIABLE,
            CallbackAction.SEND_VARIABLES,
        ],
        **kwargs
    ):
        """Constructor for a OK button which will"""
        return cls(
            text=text,
            value=value,
            button_type=button_type,
            callback_actions=callback_actions,
            **kwargs,
        )

    @classmethod
    def cancel(
        cls,
        text: str = "Cancel",
        value="cancel",
        button_type=ButtonType.WARNING,
        callback_actions: List[CallbackAction] = [
            CallbackAction.SEND_VARIABLE,
        ],
        **kwargs
    ):
        """Constructor for a cancel button which will simply close
        the dialog and set the :class:`~story_graph.models.StreamVariable` ``CANCEL`` to ``'true'``
        (but as a string!).
        """
        return cls(
            text=text,
            value=value,
            callback_actions=callback_actions,
            button_type=button_type,
            **kwargs,
        )


# @todo use typing.union which is supported by upcoming strawberry version
Content = strawberry.union("Content", [Text, Input, Checkbox])


@strawberry.type
class Dialog:
    """Triggers a popup on the frontend of the listener."""

    title: str
    content: List[Content] = strawberry.field()  # type: ignore
    buttons: List[Button]

    @classmethod
    def gps(cls, title: str = "GPS"):
        return cls(
            title=title,
            content=[Checkbox.gps()],
            buttons=[],
        )
