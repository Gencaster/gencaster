import asyncio
import random
from datetime import datetime
from typing import Dict, Optional
from unittest import mock

from asgiref.sync import async_to_sync, sync_to_async
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TransactionTestCase
from mistletoe import Document
from mixer.backend.django import mixer

from stream.models import StreamVariable

from .engine import Engine, GraphDeadEnd, InvalidPythonCode, ScriptCellTimeout
from .markdown_parser import GencasterRenderer
from .models import (
    AudioCell,
    CellType,
    Edge,
    Graph,
    Node,
    NodeDoor,
    NodeDoorMissing,
    ScriptCell,
)


class GraphTestCase(TransactionTestCase):
    @staticmethod
    def get_graph(**kwargs) -> Graph:
        return mixer.blend(Graph, **kwargs)  # type: ignore

    async def test_get_create_entry_node(self):
        graph = await Graph.objects.acreate(name="test_graph")
        await graph.acreate_entry_node()
        self.assertEqual(
            await Node.objects.filter(graph=graph).acount(),
            1,
        )
        node = await Node.objects.filter(graph=graph).afirst()
        if node is None:
            self.assertTrue(False)
        else:
            self.assertTrue(node.is_entry_node)


class NodeTestCase(TransactionTestCase):
    @staticmethod
    def get_node(**kwargs) -> Node:
        return mixer.blend(  # type: ignore
            Node,
            **kwargs,
        )  # type: ignore

    async def test_unique_entry_node(self):
        graph = await Graph.objects.acreate(name="test_graph")
        await graph.acreate_entry_node()
        self.assertEqual(await Node.objects.filter(graph=graph).acount(), 1)
        with self.assertRaises(IntegrityError):
            await Node.objects.acreate(
                graph=graph,
                name="foobar",
                is_entry_node=True,
            )


class EdgeTestCase(TransactionTestCase):
    def setUp(self) -> None:
        self.graph: Graph = mixer.blend(Graph)  # type: ignore
        self.in_node: Node = mixer.blend(Node, graph=self.graph)  # type: ignore
        self.out_node: Node = mixer.blend(Node, graph=self.graph)  # type: ignore

    @staticmethod
    def get_edge(create_nodes: bool = True, **kwargs) -> Edge:
        if create_nodes:
            node_a = NodeTestCase.get_node()
            node_b = NodeTestCase.get_node()
            kwargs["in_node_door"] = node_b.get_default_in_door()
            kwargs["out_node_door"] = node_a.get_default_out_door()
        return mixer.blend(Edge, **kwargs)  # type: ignore

    def test_fail_unique(self):
        Edge(
            in_node_door=self.in_node.get_default_in_door(),
            out_node_door=self.out_node.get_default_out_door(),
        ).save()

        # creating the same edge should fail
        with self.assertRaises(IntegrityError):
            Edge(
                in_node_door=self.in_node.get_default_in_door(),
                out_node_door=self.out_node.get_default_out_door(),
            ).save()

    def test_loop(self):
        Edge(
            in_node_door=self.in_node.get_default_in_door(),
            out_node_door=self.out_node.get_default_out_door(),
        ).save()

    def test_in_node_door_is_input_door(self):
        node = NodeTestCase.get_node()
        edge = Edge(
            in_node_door=node.get_default_out_door(),
            out_node_door=node.get_default_out_door(),
        )

        with self.assertRaises(ValidationError):
            edge.save()

        edge = Edge(
            in_node_door=node.get_default_in_door(),
            out_node_door=node.get_default_in_door(),
        )

        with self.assertRaises(ValidationError):
            edge.save()

    async def test_outgoing_edges(self):
        graph = await sync_to_async(GraphTestCase.get_graph)()
        node_a = await sync_to_async(NodeTestCase.get_node)(
            graph=graph,
        )
        node_b = await sync_to_async(NodeTestCase.get_node)(
            graph=graph,
        )
        node_door_out_a = await node_a.aget_default_out_door()
        node_door_in_b = await node_b.aget_default_in_door()
        edge = await Edge.objects.acreate(
            in_node_door=node_door_in_b,
            out_node_door=node_door_out_a,
        )
        self.assertEqual((await node_door_out_a.out_edges.afirst()).uuid, edge.uuid)  # type: ignore
        self.assertEqual((await node_door_in_b.in_edges.afirst()).uuid, edge.uuid)  # type: ignore


class NodeDoorTestCase(TransactionTestCase):
    @staticmethod
    def get_node_door(**kwargs) -> NodeDoor:
        return mixer.blend(NodeDoor, **kwargs)  # type: ignore

    def test_create_default_doors(self):
        node = NodeTestCase.get_node()
        self.assertEqual(NodeDoor.objects.count(), 2)
        default_in_door = node.get_default_in_door()
        self.assertEqual(default_in_door.door_type, NodeDoor.DoorType.INPUT)
        self.assertEqual(default_in_door.node.uuid, node.uuid)

        default_out_door = node.get_default_out_door()
        self.assertEqual(default_out_door.door_type, NodeDoor.DoorType.OUTPUT)
        self.assertEqual(default_out_door.node.uuid, node.uuid)

    def test_default_unique(self):
        node = NodeTestCase.get_node()

        with self.assertRaises(IntegrityError):
            NodeDoor(
                node=node,
                is_default=True,
                door_type=NodeDoor.DoorType.INPUT,
            ).save()

        with self.assertRaises(IntegrityError):
            NodeDoor(
                node=node,
                is_default=True,
                door_type=NodeDoor.DoorType.OUTPUT,
            ).save()

    def test_get_default_door_missing_exception(self):
        node = NodeTestCase.get_node()
        NodeDoor.objects.all().delete()
        with self.assertRaises(NodeDoorMissing):
            node.get_default_in_door()
        with self.assertRaises(NodeDoorMissing):
            node.get_default_out_door()


class GencasterMarkdownTestCase(TransactionTestCase):
    @staticmethod
    def gm_md(text: str, variables: Optional[Dict] = None) -> str:
        with GencasterRenderer(variables) as renderer:
            document = Document(text)
            ssml_text = renderer.render(document)
        return ssml_text  # type: ignore

    SPEAK = "<speak>{}</speak>"

    def test_speak(self):
        self.assertEqual(self.SPEAK.format("Hello World"), self.gm_md("Hello World"))

    def test_female(self):
        self.assertTrue("de-DE-Neural2-C" in self.gm_md("{female}`foo`"))

    def test_male(self):
        self.assertTrue("de-DE-Neural2-B" in self.gm_md("{male}`foo`"))

    def test_break(self):
        self.assertEqual(
            self.SPEAK.format('foo<break time="100ms"/>bar'),
            self.gm_md("foo{break}`100ms`bar"),
        )

    def test_eval_python(self):
        self.assertEqual(self.SPEAK.format(4), self.gm_md("{python}`2+2`"))

    def test_fail_eval_python(self):
        self.assertEqual(self.SPEAK.format(""), self.gm_md("{python}`2+`"))

    def test_unknown_token(self):
        self.assertEqual(self.SPEAK.format("foo"), self.gm_md("{bar}`foo`"))

    def test_heading_line_berak(self):
        text = """# Foo
bar.
baz.
"""
        self.assertEqual(self.SPEAK.format("Foo\nbar.\nbaz."), self.gm_md(text))

    def test_chars(self):
        self.assertTrue(
            'say-as interpret-as="characters"' in self.gm_md("{chars}`foo`")
        )

    def test_moderate(self):
        self.assertTrue('emphasis level="moderate"' in self.gm_md("{moderate}`foo`"))

    def test_var(self):
        self.assertEqual(
            self.SPEAK.format("hello world"),
            self.gm_md("hello {var}`foo`", {"foo": "world"}),
        )

    def test_var_unset(self):
        self.assertEqual(
            self.SPEAK.format("hello "),
            self.gm_md("hello {var}`foo`", {}),
        )

    def test_var_use_fallback(self):
        self.assertEqual(
            self.SPEAK.format("hello bar"),
            self.gm_md("hello {var}`foo|bar`", {}),
        )

    def test_var_skip_fallback(self):
        self.assertEqual(
            self.SPEAK.format("hello world"),
            self.gm_md("hello {var}`foo|bar`", {"foo": "world"}),
        )

    def test_raw_ssml(self):
        self.assertEqual(
            self.SPEAK.format('Hello <emphasis level="moderate">world</emphasis>'),
            self.gm_md('Hello {raw_ssml}`<emphasis level="moderate">world</emphasis>`'),
        )


class ScriptCellTestCase(TransactionTestCase):
    @staticmethod
    def get_script_cell(**kwargs) -> ScriptCell:
        return mixer.blend(ScriptCell, **kwargs)  # type: ignore

    def test_str(self):
        cell = self.get_script_cell()
        self.assertTrue(cell.cell_type in str(cell))

    def test_non_unique_multiple_orders(self):
        node = NodeTestCase.get_node()
        cell_a = self.get_script_cell(node=node, cell_order=10)
        cell_b = self.get_script_cell(node=node, cell_order=10)
        self.assertEqual(cell_a.cell_order, cell_b.cell_order)

    def test_script_cells_in_order_sequential(self):
        node = NodeTestCase.get_node()
        mixer.cycle(count=5).blend(
            ScriptCell,
            node=node,
            # create cell order in sequence
            cell_order=mixer.sequence(lambda x: x),
        )
        db_cell_order = list(
            ScriptCell.objects.filter(node=node).all().values_list("cell_order")
        )
        self.assertEqual(db_cell_order, sorted(db_cell_order))

    def test_script_cells_in_order_random(self):
        node = NodeTestCase.get_node()
        mixer.cycle(count=5).blend(
            ScriptCell,
            node=node,
            # create random order
            cell_order=mixer.sequence(lambda x: random.randint(0, 1000)),
        )
        db_cell_order = list(
            ScriptCell.objects.filter(node=node).all().values_list("cell_order")
        )
        self.assertEqual(db_cell_order, sorted(db_cell_order))


class AudioCellTestCase(TransactionTestCase):
    @staticmethod
    def get_audio_cell(**kwargs) -> AudioCell:
        return mixer.blend(AudioCell, **kwargs)  # type: ignore

    def test_str(self):
        audio_cell = self.get_audio_cell()
        self.assertTrue(str(audio_cell.audio_file) in str(audio_cell))


class EngineTestCase(TransactionTestCase):
    def setup_graph_without_start(self):
        from stream.tests import StreamTestCase

        self.graph = GraphTestCase.get_graph()
        self.node = NodeTestCase.get_node(graph=self.graph)
        self.script_cell = ScriptCellTestCase.get_script_cell(
            node=self.node, cell_type=CellType.PYTHON, is_blocking=True, cell_code="2+2"
        )
        self.stream = StreamTestCase.get_stream()

    async def test_no_start(self):
        await sync_to_async(self.setup_graph_without_start)()
        engine = Engine(self.graph, self.stream)
        # @todo use async with asyncio.timeout which
        # gets introduced in python 3.11
        with self.assertRaises(Node.DoesNotExist):
            await asyncio.wait_for(engine.start().__aiter__().__anext__(), 0.5)

    async def test_blocking(self):
        await sync_to_async(self.setup_graph_without_start)()
        entry_node = await self.graph.acreate_entry_node()
        entry_node.is_blocking_node = True
        await sync_to_async(entry_node.save)()
        engine = Engine(self.graph, self.stream)

        with self.assertRaises(asyncio.TimeoutError):
            await asyncio.wait_for(engine.start().__aiter__().__anext__(), 0.5)

    async def test_non_blocking_exhausting(self):
        await sync_to_async(self.setup_graph_without_start)()
        entry_node = await self.graph.acreate_entry_node()
        await Edge.objects.acreate(
            out_node_door=await self.node.aget_default_out_door(),
            in_node_door=await entry_node.aget_default_in_door(),
        )
        self.node.is_blocking_node = False
        await sync_to_async(self.node.save)()
        await sync_to_async(self.node.refresh_from_db)()

        engine = Engine(self.graph, self.stream)

        with self.assertRaises(StopAsyncIteration):
            await asyncio.wait_for(engine.start().__aiter__().__anext__(), 4.5)

    def setup_with_script_cell(
        self,
        cell_code: str,
        stream_variables: Optional[Dict] = None,
        cell_type: CellType = CellType.PYTHON,
        cell_kwargs: Optional[Dict] = None,
    ):
        from stream.tests import StreamTestCase

        cell_kwargs = cell_kwargs if cell_kwargs else {}

        self.graph = GraphTestCase.get_graph()
        self.stream = StreamTestCase.get_stream()
        entry_node = async_to_sync(self.graph.acreate_entry_node)
        self.script_cell = ScriptCellTestCase.get_script_cell(
            node=entry_node,
            cell_type=cell_type,
            cell_code=cell_code,
            **cell_kwargs,
        )

    async def helper_create_delayed_stream_variable(
        self, key: str, value: str, delay_time: float = 0.1
    ):
        await asyncio.sleep(delay_time)
        await StreamVariable.objects.acreate(
            stream=self.stream,
            key=key,
            value=value,
        )

    async def test_get_variables(self):
        await sync_to_async(self.setup_with_script_cell)("vars['a'] = 2+2")
        engine = Engine(self.graph, self.stream)
        with self.assertRaises(StopAsyncIteration):
            await asyncio.wait_for(engine.start().__aiter__().__anext__(), 5.5)
        v = await engine.get_stream_variables()
        self.assertEqual(v.get("a"), "4")

    async def test_wait_for_variables(self):
        """Actually this does not wait for the params from the database
        as I don't know how to sync two async test tasks.
        Instead we use the time to check if we can wait for a statement.
        """
        await sync_to_async(self.setup_with_script_cell)(
            """now = datetime.now()
while True:
    now_now = datetime.now()
    if((datetime.now() - now).total_seconds() > 0.2):
        break
    await asyncio.sleep(0.05)"""
        )
        engine = Engine(self.graph, self.stream)
        with self.assertRaises(StopAsyncIteration):
            await asyncio.wait_for(engine.start().__aiter__().__anext__(), 0.5)

    async def test_wait_for_start_variable(self):
        await sync_to_async(self.setup_with_script_cell)(
            """await wait_for_stream_variable('start')
vars['foo'] = 42"""
        )
        engine = Engine(self.graph, self.stream, raise_exceptions=True)
        start_time = datetime.now()
        with self.assertRaises(StopAsyncIteration):
            await asyncio.wait_for(
                asyncio.gather(
                    engine.start().__aiter__().__anext__(),
                    self.helper_create_delayed_stream_variable("start", "true", 0.2),
                ),
                1.0,
            )
        end_time = datetime.now()
        self.assertTrue((end_time - start_time).total_seconds() > 0.2)
        v = await engine.get_stream_variables()
        self.assertEqual(v.get("start"), "true")

    async def test_invalid_python_code(self):
        await sync_to_async(self.setup_with_script_cell)("34+aeu")
        engine = Engine(self.graph, self.stream, raise_exceptions=True)
        with self.assertRaises(NameError):
            await asyncio.wait_for(engine.start().__aiter__().__anext__(), 5.5)

    async def test_invalid_python_code_quiet(self):
        await sync_to_async(self.setup_with_script_cell)("34+aeu")
        engine = Engine(self.graph, self.stream, raise_exceptions=False)
        with self.assertRaises(StopAsyncIteration):
            await asyncio.wait_for(engine.start().__aiter__().__anext__(), 5.5)

    async def test_python_async_sleep_via_timeout(self):
        await sync_to_async(self.setup_with_script_cell)("await asyncio.sleep(0.5)")
        engine = Engine(self.graph, self.stream, raise_exceptions=True)
        with self.assertRaises(asyncio.exceptions.TimeoutError):
            await asyncio.wait_for(engine.start().__aiter__().__anext__(), 0.2)

    async def test_python_async_sleep_success(self):
        await sync_to_async(self.setup_with_script_cell)("await asyncio.sleep(0.1)")
        engine = Engine(self.graph, self.stream, raise_exceptions=True)
        with self.assertRaises(StopAsyncIteration):
            await asyncio.wait_for(engine.start().__aiter__().__anext__(), 0.2)

    async def test_python_self_calls(self):
        await sync_to_async(self.setup_with_script_cell)(
            "vars['foo'] = await self.get_stream_variables()"
        )
        await StreamVariable.objects.acreate(
            stream=self.stream,
            key="hello",
            value="world",
        )
        engine = Engine(self.graph, self.stream, raise_exceptions=True)
        with self.assertRaises(StopAsyncIteration):
            await asyncio.wait_for(engine.start().__aiter__().__anext__(), 0.2)
        v = await engine.get_stream_variables()
        self.assertEqual(v["foo"], "{'hello': 'world'}")

    async def test_python_w_o_self_calls(self):
        await sync_to_async(self.setup_with_script_cell)(
            "vars['foo'] = await get_stream_variables()"
        )
        await StreamVariable.objects.acreate(
            stream=self.stream,
            key="hello",
            value="world",
        )
        engine = Engine(self.graph, self.stream, raise_exceptions=True)
        with self.assertRaises(StopAsyncIteration):
            await asyncio.wait_for(engine.start().__aiter__().__anext__(), 0.2)
        v = await engine.get_stream_variables()
        self.assertEqual(v["foo"], "{'hello': 'world'}")

    async def test_python_set_variable(self):
        await sync_to_async(self.setup_with_script_cell)("vars['foo'] = 'bar'")
        engine = Engine(self.graph, self.stream, raise_exceptions=True)
        self.assertEqual(len((await engine.get_stream_variables()).keys()), 0)
        with self.assertRaises(StopAsyncIteration):
            await asyncio.wait_for(engine.start().__aiter__().__anext__(), 0.2)
        v = await engine.get_stream_variables()
        self.assertEqual(v["foo"], "bar")

    async def test_wait_for_no_stream_variable(self):
        await sync_to_async(self.setup_with_script_cell)("")
        await StreamVariable.objects.acreate(
            stream=self.stream,
            key="hello",
            value="world",
        )
        engine = Engine(self.graph, self.stream, raise_exceptions=True)
        with self.assertRaises(ScriptCellTimeout):
            await engine.wait_for_stream_variable("foo", timeout=0.1)

    async def test_wait_for_existing_stream_variable(self):
        await sync_to_async(self.setup_with_script_cell)("")
        await StreamVariable.objects.acreate(
            stream=self.stream,
            key="hello",
            value="world",
        )
        engine = Engine(self.graph, self.stream, raise_exceptions=True)
        await engine.wait_for_stream_variable("hello", timeout=0.1)

    async def test_wait_for_changing_stream_variable(self):
        await sync_to_async(self.setup_with_script_cell)("")
        await StreamVariable.objects.acreate(
            stream=self.stream,
            key="hello",
            value="world",
        )
        engine = Engine(self.graph, self.stream, raise_exceptions=True)
        job = asyncio.gather(
            self.helper_create_delayed_stream_variable("start", "true", 0.1),
            engine.wait_for_stream_variable("start", timeout=1.0, update_speed=0.1),
        )
        await asyncio.wait_for(job, timeout=0.5)

    async def test_yield_dialog(self):
        # if this fails please update the docs for the editor as well!
        from stream.frontend_types import Dialog

        await sync_to_async(self.setup_with_script_cell)(
            "yield Dialog(title='Hello', content=[Text(text='Hello World')], buttons=[Button.ok()])"
        )

        engine = Engine(self.graph, self.stream, raise_exceptions=True)
        x = engine.start().__aiter__()
        dialog: Dialog = await asyncio.wait_for(x.__anext__(), 0.2)  # type: ignore
        with self.assertRaises(StopAsyncIteration):
            await asyncio.wait_for(x.__anext__(), 0.2)

        self.assertEqual(dialog.title, "Hello")
        self.assertEqual(len(dialog.content), 1)
        self.assertEqual(dialog.content[0].text, "Hello World")  # type: ignore
        self.assertEqual(len(dialog.buttons), 1)
        self.assertEqual(dialog.buttons[0].text, "OK")

    @mock.patch("stream.models.StreamPoint.speak_on_stream")
    async def test_execute_markdown_code(self, speak_mock: mock.MagicMock):
        await sync_to_async(self.setup_with_script_cell)(
            "Hello world",
            None,
            cell_type=CellType.MARKDOWN,
        )
        engine = Engine(self.graph, self.stream, raise_exceptions=True)
        with mock.patch.object(engine, "wait_for_finished_instruction") as patch:
            x = engine.start().__aiter__()
            with self.assertRaises(StopAsyncIteration):
                for _ in range(2):
                    await asyncio.wait_for(x.__anext__(), 0.2)
            assert patch.called
        speak_mock.assert_called_once_with("<speak>Hello world</speak>")

    @mock.patch("stream.models.StreamPoint.send_raw_instruction")
    async def text_execute_sc_code(self, sc_instruction_mock: mock.MagicMock):
        # @todo this yields no coverage although the tests makes it obvious
        # that the code is executed
        from stream.models import StreamInstruction

        await sync_to_async(self.setup_with_script_cell)(
            "2+2",
            None,
            cell_type=CellType.SUPERCOLLIDER,
        )
        engine = Engine(self.graph, self.stream, raise_exceptions=True)
        with mock.patch.object(engine, "wait_for_finished_instruction") as patch:
            x = engine.start().__aiter__()
            with self.assertRaises(StopAsyncIteration):
                for _ in range(4):
                    await asyncio.wait_for(x.__anext__(), 0.2)
            assert patch.called
        self.assertEqual(await StreamInstruction.objects.acount(), 1)
        sc_instruction_mock.assert_called_once_with("2+2")

    @mock.patch("stream.models.StreamPoint.play_audio_file")
    async def test_execute_audio_cell(self, play_audio_file_mock: mock.MagicMock):
        audio_cell = await sync_to_async(AudioCellTestCase.get_audio_cell)()
        await sync_to_async(self.setup_with_script_cell)(
            cell_code="2+2",
            stream_variables=None,
            cell_type=CellType.AUDIO,
            cell_kwargs={"audio_cell": audio_cell},
        )
        engine = Engine(self.graph, self.stream, raise_exceptions=True)
        with mock.patch.object(engine, "wait_for_finished_instruction") as patch:
            x = engine.start().__aiter__()
            with self.assertRaises(StopAsyncIteration):
                for _ in range(4):
                    await asyncio.wait_for(x.__anext__(), 0.2)
            assert patch.called
        play_audio_file_mock.assert_called_once_with(
            audio_cell.audio_file, audio_cell.playback
        )

    async def test_wait_for_finished_instruction_timeout(self):
        from stream.models import StreamInstruction

        await sync_to_async(self.setup_with_script_cell)(
            cell_code="2+2",
            cell_type=CellType.SUPERCOLLIDER,
        )
        engine = Engine(self.graph, self.stream, raise_exceptions=True)
        instruction = StreamInstruction(
            stream_point=self.stream.stream_point,
            state=StreamInstruction.InstructionState.SENT,
            instruction_text="",
        )
        await instruction.asave()

        with self.assertRaises(asyncio.TimeoutError):
            await engine.wait_for_finished_instruction(
                instruction=instruction,
                timeout=0.01,
                interval=0.001,
            )

    async def test_wait_for_finished_instruction(self):
        from stream.models import StreamInstruction

        async def set_instruction_finished_with_delay(
            stream_instruction: StreamInstruction, delay: float
        ):
            await asyncio.sleep(delay)
            stream_instruction.state = StreamInstruction.InstructionState.FINISHED
            await stream_instruction.asave()

        await sync_to_async(self.setup_with_script_cell)(
            cell_code="2+2",
            cell_type=CellType.SUPERCOLLIDER,
        )
        engine = Engine(self.graph, self.stream, raise_exceptions=True)
        instruction = StreamInstruction(
            stream_point=self.stream.stream_point,
            state=StreamInstruction.InstructionState.SENT,
            instruction_text="",
        )
        await instruction.asave()

        job = asyncio.gather(
            set_instruction_finished_with_delay(instruction, 0.1),
            engine.wait_for_finished_instruction(
                instruction=instruction,
                timeout=1.0,
                interval=0.1,
            ),
        )
        await asyncio.wait_for(job, timeout=0.5)

        self.assertEqual((await StreamInstruction.objects.afirst()).state, StreamInstruction.InstructionState.FINISHED)  # type: ignore

    async def test_evaluate_python_code(self):
        await sync_to_async(self.setup_with_script_cell)(
            cell_code="2+2",
            cell_type=CellType.SUPERCOLLIDER,
        )
        engine = Engine(self.graph, self.stream, raise_exceptions=True)

        with self.assertRaises(InvalidPythonCode):
            await engine._evaluate_python_code("2+")

        with self.assertRaises(InvalidPythonCode):
            await engine._evaluate_python_code("'foobar'")

        self.assertTrue(await engine._evaluate_python_code("2==2"))
        self.assertFalse(await engine._evaluate_python_code("2==1"))

    async def test_get_next_node(self):
        await sync_to_async(self.setup_with_script_cell)(
            "2+2",
            None,
            cell_type=CellType.PYTHON,
        )
        engine = Engine(self.graph, self.stream, raise_exceptions=True)
        # start node
        node_a: Node = await Node.objects.afirst()  # type: ignore
        node_b = await Node.objects.acreate(
            graph=self.graph,
        )
        # make sure all default doors are there
        self.assertEqual(await NodeDoor.objects.acount(), 4)
        await Edge.objects.acreate(
            out_node_door=await node_a.aget_default_out_door(),
            in_node_door=await node_b.aget_default_in_door(),
        )
        self.assertEqual(await Edge.objects.acount(), 1)
        engine._current_node = node_a
        next_node = await engine.get_next_node()
        self.assertEqual(next_node.uuid, node_b.uuid)

    async def test_get_next_node_with_vars(self):
        await sync_to_async(self.setup_with_script_cell)(
            "2+2",
            None,
            cell_type=CellType.PYTHON,
        )
        engine = Engine(self.graph, self.stream, raise_exceptions=True)
        # start node
        node_a: Node = await Node.objects.afirst()  # type: ignore
        node_b = await Node.objects.acreate(
            graph=self.graph,
        )
        node_c = await Node.objects.acreate(
            graph=self.graph,
        )
        await Edge.objects.acreate(
            out_node_door=await node_a.aget_default_out_door(),
            in_node_door=await node_b.aget_default_in_door(),
        )
        custom_node_door = await NodeDoor.objects.acreate(
            door_type=NodeDoor.DoorType.OUTPUT,
            node=node_a,
            name="foobar",
            is_default=False,
            code="2==2",
        )

        await Edge.objects.acreate(
            out_node_door=custom_node_door,
            in_node_door=await node_c.aget_default_in_door(),
        )
        self.assertEqual(await Edge.objects.acount(), 2)
        # make sure all default doors are there
        self.assertEqual(await NodeDoor.objects.acount(), 7)

        engine._current_node = node_a
        next_node = await engine.get_next_node()
        self.assertEqual(next_node.uuid, node_c.uuid)

    async def test_failed_node_door_code(self):
        await sync_to_async(self.setup_with_script_cell)(
            "2+2",
            None,
            cell_type=CellType.PYTHON,
        )
        engine = Engine(self.graph, self.stream, raise_exceptions=True)
        # start node
        node_a: Node = await Node.objects.afirst()  # type: ignore
        node_b = await Node.objects.acreate(
            graph=self.graph,
        )
        node_c = await Node.objects.acreate(
            graph=self.graph,
        )
        await Edge.objects.acreate(
            out_node_door=await node_a.aget_default_out_door(),
            in_node_door=await node_b.aget_default_in_door(),
        )
        custom_node_door = await NodeDoor.objects.acreate(
            door_type=NodeDoor.DoorType.OUTPUT,
            node=node_a,
            name="foobar",
            is_default=False,
            code="2==",
        )

        await Edge.objects.acreate(
            out_node_door=custom_node_door,
            in_node_door=await node_c.aget_default_in_door(),
        )
        self.assertEqual(await Edge.objects.acount(), 2)
        # make sure all default doors are there
        self.assertEqual(await NodeDoor.objects.acount(), 7)

        engine._current_node = node_a
        next_node = await engine.get_next_node()
        self.assertEqual(next_node.uuid, node_b.uuid)

    async def test_node_door_code_false(self):
        await sync_to_async(self.setup_with_script_cell)(
            "2+2",
            None,
            cell_type=CellType.PYTHON,
        )
        engine = Engine(self.graph, self.stream, raise_exceptions=True)
        # start node
        node_a: Node = await Node.objects.afirst()  # type: ignore
        node_b = await Node.objects.acreate(
            graph=self.graph,
        )
        node_c = await Node.objects.acreate(
            graph=self.graph,
        )
        await Edge.objects.acreate(
            out_node_door=await node_a.aget_default_out_door(),
            in_node_door=await node_b.aget_default_in_door(),
        )
        stream_variable = await StreamVariable.objects.acreate(
            stream=self.stream,
            key="foo",
            value="bar",
        )
        custom_node_door = await NodeDoor.objects.acreate(
            door_type=NodeDoor.DoorType.OUTPUT,
            node=node_a,
            name="foobar",
            is_default=False,
            code='vars["foo"]=="bar"',
        )

        await Edge.objects.acreate(
            out_node_door=custom_node_door,
            in_node_door=await node_c.aget_default_in_door(),
        )
        self.assertEqual(await Edge.objects.acount(), 2)
        # make sure all default doors are there
        self.assertEqual(await NodeDoor.objects.acount(), 7)

        engine._current_node = node_a
        next_node = await engine.get_next_node()
        self.assertEqual(next_node.uuid, node_c.uuid)

    async def test_run_into_dead_end(self):
        await sync_to_async(self.setup_with_script_cell)(
            "2+2",
            None,
            cell_type=CellType.PYTHON,
        )
        start_node = await Node.objects.afirst()
        engine = Engine(self.graph, self.stream, raise_exceptions=True)
        engine._current_node = start_node  # type: ignore

        with self.assertRaises(GraphDeadEnd):
            await engine.get_next_node()
