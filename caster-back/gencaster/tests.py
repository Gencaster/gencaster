import logging
import uuid
from unittest import mock

from asgiref.sync import async_to_sync, sync_to_async
from django.test import TransactionTestCase

from story_graph.models import AudioCell, CellType, Edge, Graph, Node, ScriptCell
from story_graph.tests import (
    AudioCellTestCase,
    EdgeTestCase,
    GraphTestCase,
    NodeTestCase,
    ScriptCellTestCase,
)
from stream.models import AudioFile
from stream.tests import AudioFileTestCase

from . import db_logging
from .schema import schema

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class SchemaTestCase(TransactionTestCase):
    @staticmethod
    def get_login_context(is_authenticated=True):
        m = mock.AsyncMock()
        m.request.user.is_authenticated = is_authenticated
        return m

    NODE_MUTATION = """
        mutation TestMutation($name:String!, $graphUuid:UUID!, $color:String) {
            addNode(newNode: {name: $name, graphUuid: $graphUuid, color: $color})
        }
    """

    @async_to_sync
    async def test_add_node(self):
        graph = await sync_to_async(GraphTestCase.get_graph)()

        resp = await schema.execute(
            self.NODE_MUTATION,
            variable_values={"name": "foo", "graphUuid": str(graph.uuid)},
            context_value=self.get_login_context(),
        )

        self.assertIsNone(resp.errors)
        self.assertEqual(await Node.objects.all().acount(), 1)

    @async_to_sync
    async def test_add_node_no_auth(self):
        graph = await sync_to_async(GraphTestCase.get_graph)()

        resp = await schema.execute(
            self.NODE_MUTATION,
            variable_values={"name": "foo", "graphUuid": str(graph.uuid)},
            context_value=self.get_login_context(is_authenticated=False),
        )

        self.assertGreaterEqual(len(resp.errors), 1)  # type: ignore
        self.assertEqual(await Node.objects.all().acount(), 0)

    @async_to_sync
    async def test_add_node_with_color(self):
        graph = await sync_to_async(GraphTestCase.get_graph)()

        resp = await schema.execute(
            self.NODE_MUTATION,
            variable_values={
                "name": "foo",
                "graphUuid": str(graph.uuid),
                "color": "#aaa",
            },
            context_value=self.get_login_context(),
        )
        node = await Node.objects.afirst()
        self.assertIsNotNone(node)
        self.assertEqual(node.color, "#aaa")  # type: ignore

    NODE_UPDATE_MUTATION = """
    mutation updateNode($nodeUuid: UUID!, $name: String, $color: String, $positionX: Float, $positionY: Float) {
        updateNode(
            nodeUpdate: {uuid: $nodeUuid, name: $name, color: $color, positionX: $positionX, positionY: $positionY}
        )
    }
    """

    @async_to_sync
    async def test_update_node(self):
        node: Node = await sync_to_async(NodeTestCase.get_node)()

        resp = await schema.execute(
            self.NODE_UPDATE_MUTATION,
            variable_values={
                "nodeUuid": str(node.uuid),
                "name": "foo",
                "positionX": 20.0,
                "positionY": 40.0,
                "color": "#aaa",
            },
            context_value=self.get_login_context(),
        )

        self.assertEqual(await Node.objects.all().acount(), 1)
        node_db: Node = await Node.objects.afirst()  # type: ignore
        self.assertIsNotNone(node_db)
        self.assertEqual(node_db.name, "foo")
        self.assertEqual(node_db.position_x, 20.0)
        self.assertEqual(node_db.position_y, 40.0)
        self.assertEqual(node_db.color, "#aaa")

    @async_to_sync
    async def test_add_edge(self):
        graph: Graph = await sync_to_async(GraphTestCase.get_graph)()
        in_node: Node = await sync_to_async(NodeTestCase.get_node)(graph=graph)
        out_node: Node = await sync_to_async(NodeTestCase.get_node)(graph=graph)

        mutation = """
            mutation TestMutation($nodeDoorInUuid:UUID!, $nodeDoorOutUuid:UUID!) {
                addEdge(newEdge: {nodeDoorInUuid: $nodeDoorInUuid, nodeDoorOutUuid: $nodeDoorOutUuid}) {
                    uuid
                }
            }
        """

        resp = await schema.execute(
            mutation,
            variable_values={
                "nodeDoorInUuid": str((await in_node.aget_default_in_door()).uuid),
                "nodeDoorOutUuid": str((await out_node.aget_default_out_door()).uuid),
            },
            context_value=self.get_login_context(),
        )

        self.assertIsNone(resp.errors)

        self.assertEqual(await Edge.objects.all().acount(), 1)

        edge: Edge = await Edge.objects.all().afirst()  # type: ignore
        self.assertEqual((await sync_to_async(lambda: edge.in_node_door.node)()).uuid, in_node.uuid)  # type: ignore
        self.assertEqual((await sync_to_async(lambda: edge.out_node_door.node)()).uuid, out_node.uuid)  # type: ignore

    GRAPH_QUERY = """
        query TestQuery {
            graphs {
                name
            }
        }
    """

    @async_to_sync
    async def test_no_auth(self):
        resp = await schema.execute(
            self.GRAPH_QUERY,
            context_value=self.get_login_context(is_authenticated=False),
        )

        self.assertIsNone(resp.errors)

    @async_to_sync
    async def test_with_auth(self):
        resp = await schema.execute(
            self.GRAPH_QUERY,
            context_value=self.get_login_context(is_authenticated=True),
        )
        self.assertIsNone(resp.errors)
        self.assertDictEqual(resp.data, {"graphs": []})  # type: ignore

    EDGE_DELETE_MUTATION = """
        mutation TestMutation($edgeUuid: UUID!) {
            deleteEdge(edgeUuid: $edgeUuid)
        }
    """

    @async_to_sync
    async def test_delete_edge(self):
        edge: Edge = await sync_to_async(EdgeTestCase.get_edge)()

        resp = await schema.execute(
            self.EDGE_DELETE_MUTATION,
            variable_values={"edgeUuid": str(edge.uuid)},
            context_value=self.get_login_context(),
        )

        self.assertIsNone(resp.errors)
        self.assertEqual(await Edge.objects.all().acount(), 0)

    @async_to_sync
    async def test_delete_unavailable_edge(self):
        resp = await schema.execute(
            self.EDGE_DELETE_MUTATION,
            variable_values={"edgeUuid": str(uuid.uuid4())},
            context_value=self.get_login_context(),
        )
        self.assertIsNone(resp.data["deleteEdge"])  # type: ignore

    NODE_DELETE_MUTATION = """
        mutation deleteNode($nodeUuid: UUID!) {
            deleteNode(nodeUuid: $nodeUuid)
        }
    """

    @async_to_sync
    async def test_delete_node(self):
        node: Node = await sync_to_async(NodeTestCase.get_node)()

        resp = await schema.execute(
            self.NODE_DELETE_MUTATION,
            variable_values={
                "nodeUuid": str(node.uuid),
            },
            context_value=self.get_login_context(),
        )

        self.assertIsNone(resp.errors)
        self.assertEqual(await Node.objects.all().acount(), 0)

    @async_to_sync
    async def test_delete_unavailable_node(self):
        resp = await schema.execute(
            self.NODE_DELETE_MUTATION,
            variable_values={"nodeUuid": str(uuid.uuid4())},
            context_value=self.get_login_context(),
        )

        self.assertIsNone(resp.data["deleteNode"])  # type: ignore

    CREATE_SCRIPT_CELL = """
    mutation CreateScriptCells($nodeUuid: UUID!, $scriptCellInputs: [ScriptCellInputCreate!]!) {
        createScriptCells(
            nodeUuid: $nodeUuid,
            scriptCellInputs: $scriptCellInputs
        ) {
            uuid
        }
    }
    """

    NEW_SCRIPT_CELL_TEMPLATE = {
        "cellType": "PYTHON",
        "cellCode": "something",
        "cellOrder": 10,
    }

    @async_to_sync
    async def test_add_script_cell(self):
        node: Node = await sync_to_async(NodeTestCase.get_node)()

        resp = await schema.execute(
            self.CREATE_SCRIPT_CELL,
            variable_values={
                "nodeUuid": str(node.uuid),
                "scriptCellInputs": [self.NEW_SCRIPT_CELL_TEMPLATE],
            },
            context_value=self.get_login_context(),
        )

        self.assertIsNone(resp.errors)
        self.assertEqual(await ScriptCell.objects.all().acount(), 1)

    @async_to_sync
    async def test_add_script_cell_no_auth(self):
        node: Node = await sync_to_async(NodeTestCase.get_node)()

        resp = await schema.execute(
            self.CREATE_SCRIPT_CELL,
            variable_values={
                "nodeUuid": str(node.uuid),
                "newScriptCell": self.NEW_SCRIPT_CELL_TEMPLATE,
            },
        )

        self.assertIsNotNone(resp.errors)

    @async_to_sync
    async def test_add_script_cell_invalid_node(self):
        resp = await schema.execute(
            self.CREATE_SCRIPT_CELL,
            variable_values={
                "nodeUuid": str(uuid.uuid4()),
                "newScriptCell": self.NEW_SCRIPT_CELL_TEMPLATE,
            },
            context_value=self.get_login_context(),
        )

        self.assertIsNotNone(resp.errors)
        self.assertEqual(0, await ScriptCell.objects.all().acount())

    UPDATE_SCRIPT_CELL = """
    mutation UpdateScriptCells($scriptCellInputs: [ScriptCellInputUpdate!]!) {
        updateScriptCells(
            scriptCellInputs: $scriptCellInputs
        ) {
            uuid
        }
    }
    """

    @async_to_sync
    async def test_update_script_cell(self):
        script_cell: ScriptCell = await sync_to_async(
            ScriptCellTestCase.get_script_cell
        )()

        resp = await schema.execute(
            self.UPDATE_SCRIPT_CELL,
            variable_values={
                "scriptCellInputs": [
                    {
                        "uuid": str(script_cell.uuid),
                        "cellType": "MARKDOWN",
                        "cellOrder": 4,
                        "cellCode": "Hello vinzenz!",
                    }
                ],
            },
            context_value=self.get_login_context(),
        )
        self.assertIsNone(resp.errors)
        await sync_to_async(script_cell.refresh_from_db)()

        self.assertEqual("Hello vinzenz!", script_cell.cell_code)

    @async_to_sync
    async def test_update_script_cell_no_auth(self):
        script_cell: ScriptCell = await sync_to_async(
            ScriptCellTestCase.get_script_cell
        )(cell_code="Hello world!")

        resp = await schema.execute(
            self.UPDATE_SCRIPT_CELL,
            variable_values={
                "newCells": [
                    {
                        "uuid": str(script_cell.uuid),
                        "cellType": "MARKDOWN",
                        "cellOrder": 4,
                        "cellCode": "Hello vinzenz!",
                    }
                ]
            },
        )
        self.assertIsNotNone(resp.errors)
        await sync_to_async(script_cell.refresh_from_db)()

        self.assertEqual("Hello world!", script_cell.cell_code)

    @async_to_sync
    async def test_create_script_cell(self):
        node: Node = await sync_to_async(NodeTestCase.get_node)()
        self.assertEqual(await ScriptCell.objects.all().acount(), 0)
        resp = await schema.execute(
            self.CREATE_SCRIPT_CELL,
            variable_values={
                "scriptCellInputs": [
                    {
                        "cellType": "MARKDOWN",
                        "cellOrder": 4,
                        "cellCode": "Hello vinzenz!",
                    }
                ],
                "nodeUuid": str(node.uuid),
            },
            context_value=self.get_login_context(),
        )
        # does NOT yield an error!
        self.assertIsNone(resp.errors)
        self.assertEqual(await ScriptCell.objects.all().acount(), 1)

    @async_to_sync
    async def test_create_audio_script_cell_missing_audio_cell(self):
        node: Node = await sync_to_async(NodeTestCase.get_node)()
        self.assertEqual(await ScriptCell.objects.all().acount(), 0)
        resp = await schema.execute(
            self.CREATE_SCRIPT_CELL,
            variable_values={
                "scriptCellInputs": [
                    {
                        "cellType": "AUDIO",
                        "cellOrder": 4,
                        "cellCode": "Hello vinzenz!",
                    }
                ],
                "nodeUuid": str(node.uuid),
            },
            context_value=self.get_login_context(),
        )
        self.assertIsNotNone(resp.errors)
        self.assertEqual(await ScriptCell.objects.all().acount(), 0)

    @async_to_sync
    async def test_create_audio_script_cell(self):
        node: Node = await sync_to_async(NodeTestCase.get_node)()
        audio_file: AudioFile = await sync_to_async(AudioFileTestCase.get_audio_file)()

        self.assertEqual(await ScriptCell.objects.all().acount(), 0)
        resp = await schema.execute(
            self.CREATE_SCRIPT_CELL,
            variable_values={
                "scriptCellInputs": [
                    {
                        "cellType": "AUDIO",
                        "cellOrder": 4,
                        "cellCode": "Hello vinzenz!",
                        "audioCell": {
                            "playback": "ASYNC_PLAYBACK",
                            "audioFile": {"uuid": str(audio_file.uuid)},
                        },
                    }
                ],
                "nodeUuid": str(node.uuid),
            },
            context_value=self.get_login_context(),
        )
        self.assertIsNone(resp.errors)
        self.assertEqual(await ScriptCell.objects.all().acount(), 1)
        # self.assertEqual(await AudioCell.objects.all().acount(), 1)

    @async_to_sync
    async def test_create_update_audio_cell(self):
        audio_file: AudioFile = await sync_to_async(AudioFileTestCase.get_audio_file)()
        audio_cell: AudioCell = await sync_to_async(AudioCellTestCase.get_audio_cell)(
            audio_file=audio_file, volume=0.4
        )
        node: Node = await sync_to_async(NodeTestCase.get_node)()

        script_cell: ScriptCell = await sync_to_async(
            ScriptCellTestCase.get_script_cell
        )(
            node=node,
            cell_type=CellType.AUDIO,
            audio_cell=audio_cell,
        )

        self.assertEqual(await ScriptCell.objects.all().acount(), 1)
        self.assertEqual(await AudioCell.objects.all().acount(), 1)

        resp = await schema.execute(
            self.UPDATE_SCRIPT_CELL,
            variable_values={
                "scriptCellInputs": [
                    {
                        "uuid": str(script_cell.uuid),
                        "cellType": "AUDIO",
                        "cellOrder": 4,
                        "cellCode": "Hello vinzenz!",
                        "audioCell": {
                            "uuid": str(audio_cell.uuid),
                            "playback": "ASYNC_PLAYBACK",
                            "volume": 0.1,
                            "audioFile": {"uuid": str(audio_file.uuid)},
                        },
                    }
                ],
            },
            context_value=self.get_login_context(),
        )
        self.assertIsNone(resp.errors)
        self.assertEqual(await ScriptCell.objects.all().acount(), 1)
        self.assertEqual(await AudioCell.objects.all().acount(), 1)

        await sync_to_async(audio_cell.refresh_from_db)()
        self.assertEqual(audio_cell.volume, 0.1)

    DELETE_SCRIPT_CELL = """
    mutation deleteScriptCell($scriptCellUuid:UUID!) {
        deleteScriptCell(scriptCellUuid: $scriptCellUuid)
    }
    """

    @async_to_sync
    async def test_delete_script_cell(self):
        script_cell: ScriptCell = await sync_to_async(
            ScriptCellTestCase.get_script_cell
        )()
        resp = await schema.execute(
            self.DELETE_SCRIPT_CELL,
            variable_values={"scriptCellUuid": str(script_cell.uuid)},
            context_value=self.get_login_context(),
        )

        self.assertIsNone(resp.errors)
        self.assertEqual(0, await ScriptCell.objects.all().acount())

    @async_to_sync
    async def test_delete_script_cell_no_auth(self):
        script_cell: ScriptCell = await sync_to_async(
            ScriptCellTestCase.get_script_cell
        )()
        resp = await schema.execute(
            self.DELETE_SCRIPT_CELL,
            variable_values={"scriptCellUuid": str(script_cell.uuid)},
        )

        self.assertIsNotNone(resp.errors)
        self.assertEqual(1, await ScriptCell.objects.all().acount())


class DatabaseLoggingTestCase(TransactionTestCase):
    def test_log_context(self):
        from stream.tests import StreamPointTestCase

        stream_point = StreamPointTestCase.get_stream_point()
        try:
            log.manager.disable = logging.DEBUG
            # setup_logging relies on its own thread which fails to
            # setup the database for a test environment, so it can not be tested
            # setup_logging()
            with self.assertLogs(log, logging.INFO) as lm:
                with db_logging.LogContext(
                    db_logging.LogKeyEnum.STREAM_POINT,
                    stream_point,
                    log,
                ):
                    log.info("Hello world")
                log.info("No logging anymore")
        finally:
            log.manager.disable = 50
            log.filters = []

        self.assertEqual(len(lm.records), 2)
        self.assertEqual(stream_point, lm.records[0].stream_point)  # type: ignore
        with self.assertRaises(AttributeError):
            lm.records[1].stream_point  # type: ignore
