import asyncio
import random

from asgiref.sync import sync_to_async
from django.db.utils import IntegrityError
from django.test import TransactionTestCase
from mistletoe import Document
from mixer.backend.django import mixer

from .engine import Engine
from .markdown_parser import GencasterRenderer
from .models import AudioCell, CellType, Edge, Graph, Node, ScriptCell


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
    def get_edge(**kwargs) -> Edge:
        return mixer.blend(Edge, **kwargs)  # type: ignore

    def test_fail_unique(self):
        Edge(
            in_node=self.in_node,
            out_node=self.out_node,
        ).save()

        # creating the same edge should fail
        with self.assertRaises(IntegrityError):
            Edge(
                in_node=self.in_node,
                out_node=self.out_node,
            ).save()

        # but reverse is possible
        Edge(
            in_node=self.out_node,
            out_node=self.in_node,
        ).save()

    def test_loop(self):
        Edge(
            in_node=self.in_node,
            out_node=self.in_node,
        ).save()


class GencasterMarkdownTestCase(TransactionTestCase):
    @staticmethod
    def gm_md(text: str) -> str:
        with GencasterRenderer() as renderer:
            document = Document(text)
            ssml_text = renderer.render(document)
        return ssml_text  # type: ignore

    SPEAK = "<speak>{}</speak>"

    def test_speak(self):
        self.assertEqual(self.SPEAK.format("Hello World"), self.gm_md("Hello World"))

    def test_female(self):
        self.assertTrue("de-DE-Standard-A" in self.gm_md("{female}`foo`"))

    def test_male(self):
        self.assertTrue("de-DE-Standard-B" in self.gm_md("{male}`foo`"))

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
            out_node=self.node,
            in_node=entry_node,
        )
        self.node.is_blocking_node = False
        await sync_to_async(self.node.save)()
        await sync_to_async(self.node.refresh_from_db)()

        engine = Engine(self.graph, self.stream)

        with self.assertRaises(StopAsyncIteration):
            await asyncio.wait_for(engine.start().__aiter__().__anext__(), 4.5)
