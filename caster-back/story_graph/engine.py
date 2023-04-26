"""
Engine
======

"""

import asyncio
import logging
import time
from copy import deepcopy
from typing import Any, AsyncGenerator, Dict

from asgiref.sync import sync_to_async

from stream.models import Stream, StreamInstruction, StreamVariable

from .markdown_parser import md_to_ssml
from .models import AudioCell, CellType, Graph, Node, ScriptCell

log = logging.getLogger(__name__)


class Engine:
    """An engine executes a :class:`~story_graph.models.Graph` on a
    :class:`~stream.models.StreamPoint`, therefore
    iterating through the nodes and executing each.
    This is written in a purely async manner so we can handle many streams at once.
    """

    def __init__(self, graph: Graph, stream: Stream) -> None:
        self.graph: Graph = graph
        self.stream = stream
        self._current_node: Node
        self.blocking_time: int = 60 * 60 * 3

    async def get_stream_variables(self) -> Dict:
        """Could be a @property but this can be difficult in async contexts
        so we use explicit async via a getter method.
        """
        v = {}
        stream_variable: StreamVariable
        async for stream_variable in self.stream.variables.all():
            v[stream_variable.key] = stream_variable.value
        return v

    async def execute_markdown_code(self, cell_code: str):
        """Runs the code of a markdown cell by parsing its content with the
        :class:`~story_graph.markdown_parser.GencasterRenderer`.
        """
        ssml_text = md_to_ssml(cell_code)
        instruction = await sync_to_async(self.stream.stream_point.speak_on_stream)(
            ssml_text
        )
        yield instruction
        await self.wait_for_finished_instruction(instruction)

    async def execute_sc_code(
        self, cell_code: str
    ) -> AsyncGenerator[StreamInstruction, None]:
        """Executes a SuperCollider code cell"""
        instruction = await sync_to_async(
            self.stream.stream_point.send_raw_instruction
        )(cell_code)
        yield instruction
        await self.wait_for_finished_instruction(instruction)

    async def execute_audio_cell(
        self, audio_cell: AudioCell
    ) -> AsyncGenerator[StreamInstruction, None]:
        """
        Plays the associated :class:`AudioFile` of an :class:`AudioCell`.

        .. todo::

            This does not respect the different Playback formats

        """
        instruction = await sync_to_async(self.stream.stream_point.play_audio_file)(
            audio_cell.audio_file, audio_cell.playback
        )
        yield instruction
        await self.wait_for_finished_instruction(instruction)

    async def execute_python_cell(self, cell_code: str) -> Any:
        stream_variables = await self.get_stream_variables()
        old_stream_variables = deepcopy(stream_variables)
        loop = asyncio.get_running_loop()
        try:
            exec(
                cell_code,
                {
                    "__builtins__": {
                        "asyncio": asyncio,
                        "int": int,
                        "loop": loop,
                        "print": print,
                        "time": time,
                    }
                },
                stream_variables,
            )
        except Exception as e:
            print(f"Occured an exception during graph engine execution: {e}")
            raise e

        # @todo
        # * skip functions / only use scalars
        for k, v in stream_variables.items():
            # unset value is a hack b/c none maybe a desired state
            # @todo switch to async bulk create
            if old_stream_variables.get(k, "__unset_value__") != v:
                await StreamVariable.objects.aupdate_or_create(
                    stream=self.stream,
                    key=k,
                    defaults={"value": v},
                )
        return stream_variables.get("return", None)

    async def wait_for_finished_instruction(
        self, instruction: StreamInstruction, timeout: int = 30, interval: float = 0.2
    ) -> None:
        for _ in range(int(timeout / interval)):
            await sync_to_async(instruction.refresh_from_db)()
            if instruction.state == StreamInstruction.InstructionState.FINISHED:
                return
            await asyncio.sleep(interval)

    async def execute_node(
        self, node: Node, blocking_sleep_time: int = 10000
    ) -> AsyncGenerator[StreamInstruction, None]:
        """Executes a node."""
        script_cell: ScriptCell
        async for script_cell in node.script_cells.select_related("audio_cell", "audio_cell__audio_file").all():  # type: ignore
            cell_type = script_cell.cell_type
            if cell_type == CellType.COMMENT:
                continue
            elif cell_type == CellType.PYTHON:
                if script_cell.cell_code:
                    await self.execute_python_cell(script_cell.cell_code)

            elif cell_type == CellType.SUPERCOLLIDER:
                async for instruction in self.execute_sc_code(script_cell.cell_code):
                    yield instruction
            elif cell_type == CellType.MARKDOWN:
                async for instruction in self.execute_markdown_code(
                    script_cell.cell_code
                ):
                    yield instruction
            elif cell_type == CellType.AUDIO:
                if script_cell.audio_cell:
                    async for instruction in self.execute_audio_cell(
                        script_cell.audio_cell
                    ):
                        yield instruction
            else:
                log.error(f"Occured invalid/unknown CellType {cell_type}")

    async def start(
        self, max_steps: int = 1000
    ) -> AsyncGenerator[StreamInstruction, None]:
        """Starts the execution of the engine."""
        self._current_node = await self.graph.aget_entry_node()

        for _ in range(max_steps):
            log.info(f"Currently running node {self._current_node}")
            async for instruction in self.execute_node(self._current_node):
                yield instruction
            if self._current_node.is_blocking_node:
                log.info("Accessed a blocking node")
                await asyncio.sleep(self.blocking_time)

            # search for next node
            if (
                new_node := await Node.objects.filter(
                    in_edges__in_node=self._current_node
                )
                .order_by("?")
                .afirst()
            ):
                self._current_node = new_node
            else:
                log.error(
                    f"Ran into a dead end on {self.graph} on {self._current_node}"
                )
                return
            await asyncio.sleep(0.5)
