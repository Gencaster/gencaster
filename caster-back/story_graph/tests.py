from django.db.utils import IntegrityError
from django.test import TransactionTestCase
from mistletoe import Document
from mixer.backend.django import mixer

from .markdown_parser import GencasterRenderer
from .models import Edge, Graph, Node


class GraphTestCase(TransactionTestCase):
    @staticmethod
    def get_graph(**kwargs) -> Graph:
        return mixer.blend(Graph, **kwargs)  # type: ignore


class NodeTestCase(TransactionTestCase):
    @staticmethod
    def get_node(**kwargs) -> Node:
        return mixer.blend(  # type: ignore
            Node,
            **kwargs,
        )  # type: ignore


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
