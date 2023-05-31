"""
Markdown parser
===============

A :class:`~story_graph.models.ScriptCell` can hold markdown content in our own markdown
dialect to control breaks, change of speakers and emphasis but also allows us to access
variables which are defined within a :class:`stream.models.Stream`.
In the end this will be transformed into `SSML <https://en.wikipedia.org/wiki/Speech_Synthesis_Markup_Language>`_
which will be used for :class:`stream.models.TextToSpeech`

Choosing markdown as a scripting language has been made because it still can be written easily
by humans and treats written text as first class citizen.

The dialect is described in :class:`~GencasterRenderer`.

Use :func:`~md_to_ssml` to convert markdown text within a Python context.
"""

import logging
import re
from datetime import datetime
from typing import Callable, Dict, Optional

from mistletoe import Document, block_token, span_token
from mistletoe.base_renderer import BaseRenderer
from mistletoe.span_token import SpanToken

from stream.models import TextToSpeech

log = logging.getLogger(__name__)


def md_to_ssml(text: str, stream_variables: Optional[Dict[str, str]] = None) -> str:
    """Converts a md text into
    `SSML <https://en.wikipedia.org/wiki/Speech_Synthesis_Markup_Language>`_.

    :param text: Markdown text
    """
    with GencasterRenderer(stream_variables) as render:
        document = Document(text)
        ssml_text = render.render(document)
    return ssml_text  # type: ignore


class GencasterToken(SpanToken):
    pattern = re.compile(r"{(?P<type>\w*)}`(?P<value>[^`]*)`")
    parse_inner = False

    def __init__(self, match_obj: re.Match):
        self.target = match_obj.group(1)
        self.content = match_obj.group(2)


class GencasterRenderer(BaseRenderer):
    """
    Acts as a python parser for the Gencaster markdown dialect.
    """

    def __init__(self, stream_variables: Optional[Dict[str, str]] = None) -> None:
        super().__init__(GencasterToken)

        self.d = (
            datetime.now()
        )  # unused but needed so we can access it in a script cell

        self.stream_variables: Dict[str, str] = (
            stream_variables if stream_variables else {}
        )

        self.gencaster_token_resolver: Dict[str, Callable[[str], str]] = {
            "python": self.eval_python,
            "python_exec": self.exec_python,
            "chars": self.chars,
            "break": self.add_break,
            "moderate": self.moderate,
            "male": self.male,
            "female": self.female,
            "var": self.var,
        }

    def validate_gencaster_tokens(self, text: str) -> bool:
        """Validates if the used tags are known to Gencaster

        .. todo::

            this is not implemented yet and will raise an exception
        """
        raise NotImplementedError()

    def chars(self, text: str) -> str:
        """
        Speaks surrounded words as characters, so "can" becomes "C A N", see
        `say as <https://cloud.google.com/text-to-speech/docs/ssml#say%E2%80%91as>`_
        in GC docs.

        .. code-block:: markdown

            how {chars}`can` you talk

        """
        return f'<say-as interpret-as="characters">{text}</say-as>'

    def moderate(self, text: str) -> str:
        """
        Speaks surrounded words in a moderate manner, see
        `emphasis <https://cloud.google.com/text-to-speech/docs/ssml#emphasis>`_
        in GC docs.

        .. code-block:: markdown

            speak {moderate}`something` to me

        """
        return f'<emphasis level="moderate">{text}</emphasis>'

    def female(self, text: str) -> str:
        """
        Speaks as ``DE_STANDARD_A__FEMALE`` from :class:`stream.models.TextToSpeech.VoiceNameChoices`.

        .. code-block:: markdown

            hello {female}`world`

        """
        return f'<voice name="{TextToSpeech.VoiceNameChoices.DE_NEURAL2_C__FEMALE}">{text}</voice>'

    def male(self, text: str) -> str:
        """
        Speaks as ``DE_STANDARD_B__MALE`` from :class:`stream.models.TextToSpeech.VoiceNameChoices`.

        .. code-block:: markdown

            hello {male}`world`

        """
        return f'<voice name="{TextToSpeech.VoiceNameChoices.DE_NEURAL2_B__MALE}">{text}</voice>'

    # break is native word in python
    def add_break(self, text: str) -> str:
        """
        Adds a break between words, see
        `break <https://cloud.google.com/text-to-speech/docs/ssml#break>`_ in GC docs.

        Example: Add a break of 300ms between hello and world.

        .. code-block:: markdown

            hello {break}`300ms` world
        """
        return f'<break time="{text}"/>'

    def eval_python(self, text: str) -> str:
        """
        Execute a python inline script via eval, e.g.

        .. code-block:: markdown

            two plus two is {eval_python}`2+2`

        will result in `two plus two is 4`.

        Eval does not allow for variable assignment but we obtain a return value.

        .. todo::

            Store variables in :class:`story_graph.models.GraphSession` context.

        """
        try:
            r = eval(text)
            return str(r) if r is not None else ""
        except SyntaxError as e:
            log.error(f"Could not evaluate python code: {e}")
            return ""

    def exec_python(self, text: str) -> str:
        """
        Executes a Python statement which allows to assign variables.


        .. code-block:: markdown

            {exec_python}`a=2`
            A is now {eval_python}`a`.

        becomes `A is now 2`.

        .. seealso::

           Use :func:`~GencasterRenderer.var` to access stream variables.
        """
        try:
            exec(text)
        except Exception as e:
            log.error(f"Could not execute python code: {e}")
        return ""

    def var(self, text: str) -> str:
        """
        Refers to the value of a :class:`~stream.models.StreamVariable`.

        Example:

        Assuming we have set a streaming variable ``{"foo": "world"}``

        .. code-block:: markdown

            Hello {var}`foo`

        becomes `Hello World`.

        If the streaming variable does not exist it will be replaced with an
        empty string `""`, but we can provide a fallback value via ``|``.

        .. code-block:: markdown

            Hello {var}`something_unknown|foobar`

        becomes `Hello foobar` if the streaming variable ``something_unknown`` does not exist.
        """
        fallback_value = text.split("|")[-1] if text.count("|") else ""
        return self.stream_variables.get(text.split("|")[0], fallback_value)

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
        """"""
        return token.content  # type: ignore

    def render_document(self, token: block_token.Document) -> str:
        text = super().render_document(token)
        return f"<speak>{text}</speak>"
