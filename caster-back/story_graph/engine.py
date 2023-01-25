"""
Engine
======

"""

import asyncio
import logging
from typing import AsyncGenerator

from asgiref.sync import sync_to_async

from stream.models import StreamInstruction, StreamPoint

from .markdown_parser import md_to_ssml
from .models import Graph, Node, ScriptCell

log = logging.getLogger(__name__)


class Engine:
    """An engine executes a :class:`~story_graph.models.Graph` on a
    :class:`~stream.models.StreamPoint`, therefore
    iterating through the nodes and executing each.
    This is written in a purely async manner so we can handle many streams at once.
    """

    def __init__(self, graph: Graph, streaming_point: StreamPoint) -> None:
        self.graph: Graph = graph
        self.streaming_point: StreamPoint = streaming_point
        self._current_node: Node

    def execute_markdown_code(self, cell_code: str):
        """Runs the code of a markdown cell by parsing its content with the
        :class:`~story_graph.markdown_parser.GencasterRenderer`.
        """
        ssml_text = md_to_ssml(cell_code)
        self.streaming_point.speak_on_stream(ssml_text)

    async def execute_sc_code(
        self, cell_code: str
    ) -> AsyncGenerator[StreamInstruction, None]:
        """Executes a SuperCollider code cell"""
        instruction = await sync_to_async(self.streaming_point.send_raw_instruction)(
            cell_code
        )
        yield instruction
        for _ in range(10):
            await sync_to_async(instruction.refresh_from_db)()
            if instruction.state == StreamInstruction.InstructionState.FINISHED:
                return
            await asyncio.sleep(0.2)

    async def execute_node(self, node: Node) -> AsyncGenerator[StreamInstruction, None]:
        """Executes a node."""
        script_cell: ScriptCell
        async for script_cell in node.script_cells.all():  # type: ignore
            cell_type = script_cell.cell_type
            if cell_type == ScriptCell.CellType.COMMENT:
                continue
            elif cell_type == ScriptCell.CellType.PYTHON:
                print("Python should now execute: ", script_cell.cell_code)
                if script_cell.cell_code:
                    exec(script_cell.cell_code)
            elif cell_type == ScriptCell.CellType.SUPERCOLLIDER:
                async for instruction in self.execute_sc_code(script_cell.cell_code):
                    yield instruction
            elif cell_type == ScriptCell.CellType.MARKDOWN:
                await sync_to_async(self.execute_markdown_code)(script_cell.cell_code)
            else:
                log.error(f"Occured invalid/unknown CellType {cell_type}")

    async def start(
        self, max_steps: int = 1000
    ) -> AsyncGenerator[StreamInstruction, None]:
        """Starts the execution of the engine."""
        if new_node := await self.graph.get_entry_node():
            self._current_node = new_node
        else:
            log.error(
                f"Could not find entry node on {self.graph} for {self.streaming_point}"
            )
            return

        for _ in range(max_steps):
            log.debug(f"Currently running node {self._current_node}")
            if (
                new_node := await Node.objects.filter(
                    in_edges__in_node=self._current_node
                )
                .order_by("?")
                .afirst()
            ):
                self._current_node = new_node
                async for instruction in self.execute_node(self._current_node):
                    yield instruction
            else:
                log.error(
                    f"Ran into a dead end on {self.graph} on {self._current_node} - reset"
                )
                # back off a bit!
                await asyncio.sleep(30)
                if new_node := await self.graph.get_entry_node():
                    self._current_node = new_node
            await asyncio.sleep(0.5)
