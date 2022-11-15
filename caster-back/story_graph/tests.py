from django.db.utils import IntegrityError
from django.test import TransactionTestCase
from mixer.backend.django import mixer

from .models import Edge, Graph, Node


class GraphTestCase(TransactionTestCase):
    @staticmethod
    def get_graph(**kwargs) -> Graph:
        return mixer.blend(Graph, **kwargs)  # type: ignore


class NodeTestCase(TransactionTestCase):
    @staticmethod
    def get_node(**kwargs) -> Node:
        return mixer.blend(
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
