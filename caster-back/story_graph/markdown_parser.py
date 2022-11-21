import logging
import re
from datetime import datetime
from typing import Callable, Dict

from mistletoe import block_token, span_token
from mistletoe.base_renderer import BaseRenderer
from mistletoe.span_token import SpanToken

from stream.models import TextToSpeech

log = logging.getLogger(__name__)


class GencasterToken(SpanToken):
    pattern = re.compile(r"{(?P<type>\w*)}`(?P<value>[^`]*)`")
    parse_inner = False

    def __init__(self, match_obj: re.Match):
        self.target = match_obj.group(1)
        self.content = match_obj.group(2)


class GencasterRenderer(BaseRenderer):
    def __init__(self) -> None:
        super().__init__(GencasterToken)

        self.d = (
            datetime.now()
        )  # unused but needed so we can access it in a script cell

        self.gencaster_token_resolver: Dict[str, Callable[[str], str]] = {
            "python": self._eval_python,
            "python_exec": self._exec_python,
            "chars": self._chars,
            "break": self._break,
            "moderate": self._moderate,
            "male": self._male,
            "female": self._female,
        }

    def validate_gencaster_tokens(self, text: str) -> bool:
        """Validates if the used tags are known to GenCaster"""
        # @todo this is not implemented and should raise an exception
        return True

    def _chars(self, text: str) -> str:
        return f'<say-as interpret-as="characters">{text}</say-as>'

    def _moderate(self, text: str) -> str:
        return f'<emphasis level="moderate">{text}</emphasis>'

    def _female(self, text: str) -> str:
        return f'<voice name="{TextToSpeech.VoiceNameChoices.DE_STANDARD_A__FEMALE}">{text}</voice>'

    def _male(self, text: str) -> str:
        return f'<voice name="{TextToSpeech.VoiceNameChoices.DE_STANDARD_B__MALE}">{text}</voice>'

    def _break(self, text: str) -> str:
        return f'<break time="{text}"/>'

    def _eval_python(self, text: str) -> str:
        # @todo switch to session environment
        try:
            r = eval(text)
            return str(r) if r is not None else ""
        except SyntaxError as e:
            log.error(f"Could not evaluate python code: {e}")
            return ""

    def _exec_python(self, text: str) -> str:
        try:
            exec(text)
        except Exception as e:
            log.error(f"Could not execute python code: {e}")
        return ""

    def render_gencaster_token(self, token: GencasterToken) -> str:
        try:
            return self.gencaster_token_resolver[token.target](token.content)
        except KeyError:
            log.error(f"Could not match token type {token.target}: {token.content}")
        return f"{token.content}"

    def render_heading(self, token: block_token.Heading) -> str:
        return f"{self.render_inner(token)}\n"

    def render_line_break(self, token: span_token.LineBreak) -> str:
        return "\n"

    def render_raw_text(self, token: span_token.RawText) -> str:
        return token.content  # type: ignore

    def render_document(self, token: block_token.Document) -> str:
        text = super().render_document(token)
        return f"<speak>{text}</speak>"
