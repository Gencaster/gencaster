from enum import Enum
from typing import List, Optional

import strawberry
import strawberry.django


@strawberry.enum
class ButtonType(Enum):
    DEFAULT = "default"
    PRIMARY = "primary"


@strawberry.type
class Text:
    text: str


@strawberry.type
class Button:
    text: str
    button_type: ButtonType = ButtonType.DEFAULT
    send_variables_on_click: bool = False
    send_on_click: Optional[str] = None


@strawberry.type
class Dialog:
    title: str
    content: Text
    footer: List[Button]
