"""
Engine
======

"""

import asyncio
import logging
import time
from copy import deepcopy
from datetime import datetime, timedelta
from typing import Any, AsyncGenerator, Dict, Optional, Union

from asgiref.sync import sync_to_async

from stream.frontend_types import Button, Checkbox, Dialog, Input, Text
from stream.models import Stream, StreamInstruction, StreamVariable

from .markdown_parser import md_to_ssml
from .models import AudioCell, CellType, Graph, Node, NodeDoor, ScriptCell

log = logging.getLogger(__name__)


class ScriptCellTimeout(Exception):
    pass


class GraphDeadEnd(Exception):
    pass


class InvalidPythonCode(Exception):
    pass


class Engine:
    """An engine executes a :class:`~story_graph.models.Graph` for a given
    :class:`~stream.models.StreamPoint`.
    Executing means to iterate over the :class:`~story_graph.models.Node`
    and executing each :class:`~story_graph.models.ScriptCell` within such a node.

    The engine runs in an async manner so it is possible to do awaits without
    blocking the server, which means execution is halted until a specific
    condition is met.
    """

    def __init__(
        self, graph: Graph, stream: Stream, raise_exceptions: bool = False
    ) -> None:
        self.graph: Graph = graph
        self.stream = stream
        self._current_node: Node
        self.blocking_time: int = 60 * 60 * 3
        self.raise_exceptions = raise_exceptions
        log.debug(f"Started engine for graph {self.graph.uuid}")

    async def get_stream_variables(self) -> Dict[str, str]:
        """
        Returns the associated :class:`~stream.models.StreamVariable` within
        this :class:`~stream.models.Stream` session.

        .. todo::

            Could be a @property but this can be difficult in async contexts
            so we use explicit async via a getter method.
        """
        v = {}
        stream_variable: StreamVariable
        async for stream_variable in self.stream.variables.all():
            v[stream_variable.key] = stream_variable.value
        return v

    async def wait_for_stream_variable(
        self, name: str, timeout: float = 100.0, update_speed: float = 0.5
    ):
        """Waits for a stream variable to be set.
        If the variable was not found/set within the time period of
        ``timeout`` this function will raise the exception
        :class:`ScriptCellTimeout`.

        .. danger::

            Within a script cell it is necessary to await this async function

            .. code-block:: python

                await wait_for_stream_variable('start')

        """
        log.debug(f"Wait for stream variable {name}")
        start_time = datetime.now()
        while True:
            if (datetime.now() - start_time).seconds > timeout:
                raise ScriptCellTimeout()
            if name in (await self.get_stream_variables()).keys():
                break
            await asyncio.sleep(update_speed)

    async def execute_markdown_code(self, cell_code: str):
        """Runs the code of a markdown cell by parsing its content with the
        :class:`~story_graph.markdown_parser.GencasterRenderer`.
        """
        log.debug(f"Execute markdown code '{cell_code}'")
        ssml_text = md_to_ssml(cell_code, await self.get_stream_variables())
        instruction = await sync_to_async(self.stream.stream_point.speak_on_stream)(
            ssml_text
        )
        yield instruction
        await self.wait_for_finished_instruction(instruction)

    async def execute_sc_code(
        self, cell_code: str
    ) -> AsyncGenerator[StreamInstruction, None]:
        """Executes a SuperCollider code cell"""
        log.debug(f"Run SuperCollider code '{cell_code}'")
        instruction = await sync_to_async(
            self.stream.stream_point.send_raw_instruction
        )(cell_code)
        yield instruction
        await self.wait_for_finished_instruction(instruction)

    async def execute_audio_cell(
        self, audio_cell: AudioCell
    ) -> AsyncGenerator[StreamInstruction, None]:
        """
        Plays the associated :class:`~stream.models.AudioFile` of an :class:`~story_graph.models.AudioCell`.

        .. todo::

            This does not respect the different Playback formats

        """
        # text field has no enum restrictions but the database enforces this
        log.debug(f"Run audio cell {audio_cell.uuid}")
        instruction = await sync_to_async(self.stream.stream_point.play_audio_file)(
            audio_cell.audio_file, audio_cell.playback  # type: ignore
        )
        yield instruction
        await self.wait_for_finished_instruction(instruction)

    @staticmethod
    def get_engine_global_vars(
        runtime_values: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Dict[str, Any]]:
        """Generates the dictionary which contains all objects which are available for the execution engine of
        the graph.
        This acts as a security measurement.

        .. important::

            If anything is changed here please execute

            .. code::

                make engine-variables-json

            which will create an updated autocomplete JSON for the editor.

        :param runtime_values: Allows to add additional objects to the module namespace at runtime.
            These are injected within :func:`~story_graph.engine.Engine.execute_python_cell` and consist of

            .. list-table:: Runtime vars
                :header-rows: 1

                * - key
                  - value
                  - info
                * - ``loop``
                  - loop
                  - the current asyncio loop - can be used to execute
                    additional async code
                * - ``vars``
                  - a dictionary of all stream variables
                  - See :func:`~story_graph.engine.Engine.get_stream_variables`
                * - ``self``
                  - Current :class:`~story_graph.engine.Engine` instance
                  -
                * - ``get_stream_variables``
                  - Callable
                  - See :func:`~story_graph.engine.Engine.get_stream_variables`
                * - ``wait_for_stream_variable``
                  - Callable
                  - See :func:`~story_graph.engine.Engine.wait_for_stream_variable`

        """
        runtime_values = runtime_values if runtime_values else {}
        return {
            "__builtins__": {
                "asyncio": asyncio,
                "int": int,
                "float": float,
                "print": print,
                "time": time,
                "datetime": datetime,
                "timedelta": timedelta,
                "Text": Text,
                "Dialog": Dialog,
                "Button": Button,
                "Checkbox": Checkbox,
                "Input": Input,
                **runtime_values,
            }
        }

    async def execute_python_cell(self, cell_code: str) -> AsyncGenerator[Dialog, None]:
        """Executes a python :class:`~story_graph.models.ScriptCell`.
        A python cell is run as an async generator, which allows to not just run
        synchronous code but also asynchronous mode.

        It is possible to yield immediate results from this.
        Currently only the yielding of a :class:`~stream.frontend_types.Dialog`
        instance is possible, but this could be extended.

        In order to secure at least a little bit the execution within such a script
        cell everything that is a available for execution needs to be stated
        explicitly here.
        """
        log.debug(f"Run python code '{cell_code}'")
        stream_variables = await self.get_stream_variables()
        old_stream_variables = deepcopy(stream_variables)
        loop = asyncio.get_running_loop()
        try:
            loc: Dict[str, Any] = {}
            exec(
                # wrap the script cell in an async function
                f"async def __ex(): "
                + "".join(f"\n {l}" for l in (cell_code.split("\n") + ["yield None"])),
                # global variables which are module scoped - they can not be
                # overwritten, avoiding any kind of messing with the
                # internal engine
                self.get_engine_global_vars(
                    {
                        # please note any runtime variables changes also in
                        # story_graph/management/commands/get_engine_vars.py
                        # as this will generate the necessary JSON for
                        # the autocomplete within the editor
                        "loop": loop,
                        "vars": stream_variables,
                        "self": self,
                        "get_stream_variables": self.get_stream_variables,
                        "wait_for_stream_variable": self.wait_for_stream_variable,
                    }
                ),
                # locals which mirror the current namespace and allow for modification
                # and storing of values
                loc,
            )

            # execute the wrapped async script cell code in our asyncio runtime
            # yielding allows to yield such things like a request for a Dialog
            async for x in loc["__ex"]():
                # avoid yielding none
                if x:
                    yield x
        except Exception as e:
            log.error(f"Occured an exception during graph engine execution: {e}")
            if self.raise_exceptions:
                raise e

        # @todo
        # * skip functions / only use scalars
        for k, v in stream_variables.items():
            # unset value is a hack b/c none maybe a desired state
            # @todo switch to async bulk create
            if old_stream_variables.get(k, "__unset_value__") != v:
                log.debug(f"New stream variable: {k} -> {v}")
                await StreamVariable.objects.aupdate_or_create(
                    stream=self.stream,
                    key=k,
                    defaults={"value": v},
                )
        stream_variables.get("return", None)

    async def wait_for_finished_instruction(
        self,
        instruction: StreamInstruction,
        timeout: float = 300.0,
        interval: float = 0.2,
    ) -> None:
        log.debug(f"Wait for finished instruction {instruction.uuid}")
        for _ in range(int(timeout / interval)):
            await sync_to_async(instruction.refresh_from_db)()
            if instruction.state == StreamInstruction.InstructionState.FINISHED:
                return
            await asyncio.sleep(interval)
        log.info(f"Timed out on waiting for stream instruction {instruction.uuid}")
        raise asyncio.TimeoutError()

    async def execute_node(
        self, node: Node, blocking_sleep_time: int = 10000
    ) -> AsyncGenerator[Union[StreamInstruction, Dialog], None]:
        """Executes all :class:`~story_graph.models.ScriptCell` of
        a given :class:`~story_graph.models.Node`."""
        log.debug(f"Executing node {node.uuid}")
        script_cell: ScriptCell
        instruction: Union[StreamInstruction, Dialog]
        async for script_cell in node.script_cells.select_related("audio_cell", "audio_cell__audio_file").all():  # type: ignore
            cell_type = script_cell.cell_type
            if cell_type == CellType.COMMENT:
                continue
            elif cell_type == CellType.PYTHON:
                if script_cell.cell_code:
                    async for instruction in self.execute_python_cell(
                        script_cell.cell_code
                    ):
                        yield instruction

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

    async def _evaluate_python_code(self, code: str) -> bool:
        stream_variables = await self.get_stream_variables()
        try:
            r = eval(
                code,
                self.get_engine_global_vars(
                    {
                        "loop": asyncio.get_event_loop(),
                        "vars": stream_variables,
                        "self": self,
                        "get_stream_variables": self.get_stream_variables,
                        "wait_for_stream_variable": self.wait_for_stream_variable,
                    }
                ),
            )
        except Exception:
            raise InvalidPythonCode()
        if not isinstance(r, bool):
            log.debug(f"Return type of '{code}' is not a boolean but {type(r)}")
            raise InvalidPythonCode()
        return r

    async def get_next_node(self) -> Node:
        """Iterates over each exit :class:`~NodeDoor`
        of the current node and evaluates its boolean value
        and decides.

        If the node door code consists of invalid code it will be skipped.
        If all boolean evaluations result in ``False`` or invalid code,
        the default exit will be used.

        If multiple out-going edges are connected to an active door,
        a random edge will be picked to follow for the next node.

        If the node does not have any out-going edges a :class:`~GraphDeadEnd`
        exception will be raised.
        """
        exit_door: Optional[NodeDoor]
        async for node_door in NodeDoor.objects.filter(
            node=self._current_node,
            door_type=NodeDoor.DoorType.OUTPUT,
        ).prefetch_related("node"):
            try:
                active_exit = await self._evaluate_python_code(node_door.code)
            # a broad exception because many things can go wrong here while evaluating
            # python code (e.g. even raising a custom exception), therefore we catch all
            # possible exceptions here
            except Exception:
                log.debug(
                    f"Exception raised on evaluating code of node door {node_door}"
                )
                continue
            if active_exit:
                log.debug(f"Choose exit {node_door} on {self._current_node}")
                exit_door = node_door
                break
        else:
            log.debug(f"Fallback to default node door on {self._current_node}")
            exit_door = await NodeDoor.objects.filter(
                node=self._current_node,
                door_type=NodeDoor.DoorType.OUTPUT,
                is_default=True,
            ).afirst()
        # else return default out

        if exit_door is None:
            raise GraphDeadEnd()

        try:
            return (await exit_door.out_edges.order_by("?").select_related("in_node_door__node").afirst()).in_node_door.node  # type: ignore
        except AttributeError:
            raise GraphDeadEnd()

    async def start(
        self, max_steps: int = 1000
    ) -> AsyncGenerator[Union[StreamInstruction, Dialog, GraphDeadEnd], None]:
        """Starts the execution of the engine.
        This method is an async generator which eithor yields a
        :class:`~stream.models.StreamInstruction`
        or a :class:`~stream.frontend_types.Dialog`.

        .. note::

            In order to avoid a clumping of the database a lay off period
            of 0.1 seconds is added between jumping nodes.
        """
        self._current_node = await self.graph.aget_entry_node()

        for _ in range(max_steps):
            async for instruction in self.execute_node(self._current_node):
                yield instruction
            if self._current_node.is_blocking_node:
                log.info("Accessed a blocking node")
                await asyncio.sleep(self.blocking_time)

            # search for next node
            try:
                await self.get_next_node()
            except GraphDeadEnd:
                log.info(f"Ran into a dead end on {self.graph} on {self._current_node}")
                return
            await asyncio.sleep(0.1)
        else:
            log.info(f"Reached maximum steps on graph {self.graph} - stop execution")
