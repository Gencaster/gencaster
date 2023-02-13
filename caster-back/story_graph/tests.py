import random

from django.db.utils import IntegrityError
from django.test import TransactionTestCase
from mistletoe import Document
from mixer.backend.django import mixer

from .markdown_parser import GencasterRenderer
from .models import Edge, Graph, Node, ScriptCell


class GraphTestCase(TransactionTestCase):
    @staticmethod
    def get_graph(**kwargs) -> Graph:
        return mixer.blend(Graph, **kwargs)  # type: ignore

    async def test_get_create_entry_node(self):
        graph = await Graph.objects.acreate(name="test_graph")
        await graph.aget_or_create_entry_node()
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
        await graph.aget_or_create_entry_node()
        self.assertEqual(await Node.objects.filter(graph=graph).acount(), 1)
        with self.assertRaises(IntegrityError):
            await Node.objects.acreate(
                graph=graph,
                name="foobar",
                is_entry_node=True,
            )


class EdgeTestCase(TransactionTestCase):
    def setUp(self) -> None:
        self.graph: Graph = mixer.blend(Graph)
        self.in_node: Node = mixer.blend(Node, graph=self.graph)
        self.out_node: Node = mixer.blend(Node, graph=self.graph)

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
