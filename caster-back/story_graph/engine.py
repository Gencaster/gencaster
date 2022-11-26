import asyncio
import logging

from asgiref.sync import sync_to_async

from stream.models import StreamInstruction, StreamPoint

from .markdown_parser import md_to_ssml
from .models import Graph, Node, ScriptCell

log = logging.getLogger(__name__)


class Engine:
    def __init__(self, graph: Graph, streaming_point: StreamPoint) -> None:
        self.graph: Graph = graph
        self.streaming_point: StreamPoint = streaming_point
        self._current_node: Node

    def execute_markdown_code(self, cell_code: str):
        ssml_text = md_to_ssml(cell_code)
        self.streaming_point.speak_on_stream(ssml_text)

    async def execute_sc_code(self, cell_code: str):
        instruction = await sync_to_async(self.streaming_point.send_raw_instruction)(
            cell_code
        )
        for _ in range(100):
            await sync_to_async(instruction.refresh_from_db)()
            if instruction.state == StreamInstruction.InstructionState.FINISHED:
                print("Finished executing")
                return
            await asyncio.sleep(0.2)
        print("Could not finish")

    async def execute_node(self, node: Node):
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
                await self.execute_sc_code(script_cell.cell_code)
            elif cell_type == ScriptCell.CellType.MARKDOWN:
                await sync_to_async(self.execute_markdown_code)(script_cell.cell_code)
            else:
                log.error(f"Occured invalid/unknown CellType {cell_type}")

    async def start(self):
        if new_node := await self.graph.get_entry_node():
            self._current_node = new_node
        else:
            print("Could not find entry node :/")
            return

        for _ in range(10):
            print(self._current_node)
            if (
                new_node := await Node.objects.filter(
                    out_edges__out_node=self._current_node
                )
                .order_by("?")
                .afirst()
            ):
                self._current_node = new_node
                await self.execute_node(self._current_node)
            else:
                print("Got nowhere to go?")
            await asyncio.sleep(0.5)
