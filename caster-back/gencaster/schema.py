"""
Schema
======

Here we define all the endpoints for GraphQL.

For a specific details of the types consider the
`GraphiQL <https://github.com/graphql/graphiql>`_
page available under the `/graphql` endpoint of
the running backend.

Any subscription updates are messaged via Redis and
is handled via channels and has an abstraction layer
:class:`~gencaster.distributor.GenCasterChannel`.
"""

import json
import logging
import os
import uuid
from typing import Any, AsyncGenerator, Dict, List, Optional

import strawberry
import strawberry.django
from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User as UserModel
from django.core.exceptions import PermissionDenied
from django.core.files import File
from django.http.request import HttpRequest
from strawberry import UNSET, auto
from strawberry.types import Info
from strawberry_django.fields.field import StrawberryDjangoField

import story_graph.models as story_graph_models
import stream.models as stream_models
from story_graph.engine import Engine
from story_graph.types import (
    AddGraphInput,
    AudioCellInput,
    Edge,
    EdgeInput,
    Graph,
    GraphFilter,
    InvalidPythonCode,
    Node,
    NodeCreate,
    NodeDoor,
    NodeDoorInputCreate,
    NodeDoorInputUpdate,
    NodeDoorResponse,
    NodeUpdate,
    ScriptCell,
    ScriptCellInputCreate,
    ScriptCellInputUpdate,
    UpdateGraphInput,
    create_python_highlight_string,
)
from stream.exceptions import NoStreamAvailableException
from stream.frontend_types import Dialog
from stream.types import (
    AddAudioFile,
    AudioFile,
    AudioFileUploadResponse,
    GraphDeadEnd,
    InvalidAudioFile,
    NoStreamAvailable,
    Stream,
    StreamInfo,
    StreamInfoResponse,
    StreamLog,
    StreamPoint,
    StreamVariable,
    StreamVariableInput,
    UpdateAudioFile,
)

from . import db_logging
from .distributor import GenCasterChannel, GraphQLWSConsumerInjector

log = logging.getLogger(__name__)


class IsAuthenticated(strawberry.BasePermission):
    message = "User is not authenticated"

    async def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        return True

        if await sync_to_async(lambda: info.context.request.user.is_authenticated)():  # type: ignore
            return True
        return False


class AuthStrawberryDjangoField(StrawberryDjangoField):
    """Allows us to restrict certain actions to logged in users."""

    def resolver(self, info: Info, source, **kwargs):
        request: HttpRequest = info.context.request
        if not request.user.is_authenticated:
            raise PermissionDenied()
        return super().resolver(info, source, **kwargs)


async def graphql_check_authenticated(info: Info):
    """Helper function to determine if we are loggin in an async manner.

    This would be better a decorator but strawberry is not nice in these regards, see
    `Stack Overflow <https://stackoverflow.com/a/72796313/3475778>`_.
    """
    auth = await sync_to_async(lambda: info.context.request.user.is_authenticated)()  # type: ignore
    if auth is False:
        raise PermissionDenied()


async def update_or_create_audio_cell(
    audio_cell_input: Optional[AudioCellInput],
) -> Optional[story_graph_models.AudioCell]:
    """Async function to update audio cells"""
    if audio_cell_input:
        (
            audio_cell,
            created,
        ) = await story_graph_models.AudioCell.objects.aupdate_or_create(
            uuid=audio_cell_input.uuid,
            defaults={
                "playback": audio_cell_input.playback,
                "audio_file_id": audio_cell_input.audio_file.uuid,
                "volume": audio_cell_input.volume,
            },
        )
        if created:
            # @todo access .uuid directly to avoid fk access
            # in async mode
            log.debug(f"Created audio cell {audio_cell.uuid}")
    else:
        audio_cell = None
    return audio_cell


@strawberry.django.type(UserModel)
class User:
    username: auto
    is_staff: auto
    is_active: auto
    first_name: auto
    last_name: auto
    email: auto


@strawberry.type
class Query:
    """Queries for Gencaster."""

    stream_point: StreamPoint = strawberry.django.field()
    stream_points: List[StreamPoint] = strawberry.django.field()
    graphs: List[Graph] = strawberry.django.field(filters=GraphFilter)
    graph: Graph = AuthStrawberryDjangoField()
    nodes: List[Node] = AuthStrawberryDjangoField()
    node: Node = AuthStrawberryDjangoField()
    audio_files: List[AudioFile] = AuthStrawberryDjangoField()
    audio_file: AudioFile = AuthStrawberryDjangoField()
    stream_variable: StreamVariable = AuthStrawberryDjangoField()

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def is_authenticated(self, info) -> Optional[User]:
        # type issue https://github.com/python/mypy/issues/9590
        if not await sync_to_async(lambda: info.context.request.user.is_anonymous)():  # type: ignore
            return info.context.request.user  # type: ignore
        return None


@strawberry.type
class LoginError:
    error_message: Optional[str] = None


LoginRequest = strawberry.union("LoginRequestResponse", [LoginError, User])


@strawberry.type
class Mutation:
    """Mutations for Gencaster via GraphQL."""

    @strawberry.mutation
    async def auth_login(self, info, username: str, password: str) -> LoginRequest:  # type: ignore
        # user type is Optional[AbstractBaseUser] but we return user which is similar
        user: Optional[AbstractBaseUser]
        try:
            user = await sync_to_async(authenticate)(
                request=info.context.request,
                username=username,
                password=password,
            )
        except PermissionDenied as e:
            return LoginError(
                error_message=str(e),
            )
        if user is not None:
            await sync_to_async(login)(info.context.request, user)
            return user  # type: ignore

        return LoginError(
            error_message="Wrong credentials",
        )

    @strawberry.mutation
    async def auth_logout(self, info) -> bool:
        await sync_to_async(logout)(info.context.request)
        return True

    @strawberry.mutation
    async def update_audio_file(
        self, info, uuid: uuid.UUID, update_audio_file: UpdateAudioFile
    ) -> AudioFile:
        """Update metadata of an :class:`~stream.models.AudioFile` via a UUID"""
        await graphql_check_authenticated(info)

        audio_file = await stream_models.AudioFile.objects.aget(uuid=uuid)
        if update_audio_file.name:
            audio_file.name = update_audio_file.name
        if update_audio_file.description:
            audio_file.description = update_audio_file.description
        await audio_file.asave()
        return audio_file  # type: ignore

    @strawberry.mutation
    async def add_node(self, info: Info, new_node: NodeCreate) -> None:
        """Creates a new :class:`~story_graph.models.Node` in a given
        ~class:`~story_graph.models.Graph`.
        Although it creates a new node with UUID we don't hand it back yet.
        """
        await graphql_check_authenticated(info)

        graph = await story_graph_models.Graph.objects.aget(uuid=new_node.graph_uuid)
        node = story_graph_models.Node(
            name=new_node.name,
            graph=graph,
        )

        # transfer from new_node to node model if attribute is not none
        for field in ["position_x", "position_y", "color"]:
            if new_value := getattr(new_node, field):
                setattr(node, field, new_value)

        await node.asave()
        return None

    @strawberry.mutation
    async def update_node(self, info: Info, node_update: NodeUpdate) -> None:
        """Updates a given :class:`~story_graph.models.Node` which can be used
        for renaming or moving it across the canvas.
        """
        await graphql_check_authenticated(info)

        node = await story_graph_models.Node.objects.select_related("graph").aget(
            uuid=node_update.uuid
        )

        for field in ["position_x", "position_y", "color", "name"]:
            if new_value := getattr(node_update, field):
                setattr(node, field, new_value)

        await node.asave()
        return None

    @strawberry.mutation
    async def add_edge(self, info: Info, new_edge: EdgeInput) -> Edge:
        """Creates a :class:`~story_graph.models.Edge` for a given
        :class:`~story_graph.models.Graph`.
        It returns the created edge.
        """
        await graphql_check_authenticated(info)
        in_node_door = await story_graph_models.NodeDoor.objects.select_related(
            "node__graph"
        ).aget(uuid=new_edge.node_door_in_uuid)
        out_node_door = await story_graph_models.NodeDoor.objects.aget(
            uuid=new_edge.node_door_out_uuid
        )
        edge = await story_graph_models.Edge.objects.acreate(
            in_node_door=in_node_door,
            out_node_door=out_node_door,
        )
        return edge  # type: ignore

    @strawberry.mutation
    async def delete_edge(self, info, edge_uuid: uuid.UUID) -> None:
        """Deletes a given :class:`~story_graph.models.Edge`."""
        await graphql_check_authenticated(info)
        await story_graph_models.Edge.objects.filter(uuid=edge_uuid).adelete()

    @strawberry.mutation
    async def delete_node(self, info, node_uuid: uuid.UUID) -> None:
        """Deletes a given :class:`~story_graph.models.Node`."""
        await graphql_check_authenticated(info)
        await story_graph_models.Node.objects.filter(uuid=node_uuid).adelete()

    @strawberry.mutation
    async def create_script_cells(
        self,
        info,
        script_cell_inputs: List[ScriptCellInputCreate],
        node_uuid: uuid.UUID,
    ) -> List[ScriptCell]:
        """Creates or updates a given :class:`~story_graph.models.ScriptCell` to change its content."""
        await graphql_check_authenticated(info)

        try:
            node: story_graph_models.Node = await story_graph_models.Node.objects.aget(
                uuid=node_uuid
            )
        except story_graph_models.Node.DoesNotExist as e:
            log.error(f"Received update on unknown node {node_uuid}")
            raise e

        script_cells: List[story_graph_models.ScriptCell] = []

        for script_cell_input in script_cell_inputs:
            audio_cell = await update_or_create_audio_cell(script_cell_input.audio_cell)

            # if no cell order is given we add it to the end of the current node
            if not script_cell_input.cell_order:
                cur_max_cell_order = (
                    await story_graph_models.ScriptCell.objects.filter(node=node)
                    .order_by("-cell_order")
                    .afirst()
                )
                if cur_max_cell_order:
                    script_cell_input.cell_order = cur_max_cell_order.cell_order + 1
                else:
                    script_cell_input.cell_order = 0

            script_cell = await story_graph_models.ScriptCell.objects.acreate(
                cell_order=script_cell_input.cell_order,
                cell_type=script_cell_input.cell_type,
                cell_code=script_cell_input.cell_code,
                node=node,
                audio_cell=audio_cell,
            )

            log.debug(f"Created script cell {script_cell.uuid}")
            script_cells.append(script_cell)

        return script_cells  # type: ignore

    @strawberry.mutation
    async def update_script_cells(
        self, info, script_cell_inputs: List[ScriptCellInputUpdate]
    ) -> List[ScriptCell]:
        script_cells: List[story_graph_models.ScriptCell] = []

        for script_cell_input in script_cell_inputs:
            # the async orm is still strange sometimes, therefore the code is not written in a clean
            # and concise manner
            script_cell: story_graph_models.ScriptCell = (
                await story_graph_models.ScriptCell.objects.aget(
                    uuid=script_cell_input.uuid
                )
            )
            audio_cell = await update_or_create_audio_cell(script_cell_input.audio_cell)

            # **{k: v for (k, v) in updates.items() if v is not None}
            # did not work

            updates: Dict[str, Any] = {}
            if (order := script_cell_input.cell_order) != UNSET:
                updates["cell_order"] = order
            if audio_cell:
                updates["audio_cell"] = audio_cell
            if cell_code := script_cell_input.cell_code:
                updates["cell_code"] = cell_code
            if cell_type := script_cell_input.cell_type:
                updates["cell_type"] = cell_type
            if len(updates) == 0:
                # maybe
                continue
            await story_graph_models.ScriptCell.objects.filter(
                uuid=script_cell_input.uuid
            ).aupdate(**updates)
            script_cells.append(script_cell)

        return script_cells  # type: ignore

    @strawberry.mutation
    async def delete_script_cell(self, info, script_cell_uuid: uuid.UUID) -> None:
        """Deletes a given :class:`~story_graph.models.ScriptCell`."""
        await graphql_check_authenticated(info)

        await story_graph_models.ScriptCell.objects.filter(
            uuid=script_cell_uuid
        ).adelete()

    @strawberry.mutation
    async def add_graph(self, info, graph_input: AddGraphInput) -> Graph:
        await graphql_check_authenticated(info)

        graph = await story_graph_models.Graph.objects.acreate(
            name=graph_input.name,
            display_name=graph_input.display_name,
            slug_name=graph_input.slug_name,
            start_text=graph_input.start_text,
            about_text=graph_input.about_text,
            end_text=graph_input.end_text,
            public_visible=graph_input.public_visible,
            stream_assignment_policy=graph_input.stream_assignment_policy,
        )
        await graph.acreate_entry_node()
        # need a refresh - in django 4.2 this will be available, see
        # https://docs.djangoproject.com/en/4.2/ref/models/instances/#django.db.models.Model.arefresh_from_db
        return await story_graph_models.Graph.objects.aget(uuid=graph.uuid)  # type: ignore

    @strawberry.mutation
    async def update_graph(
        self, info, graph_input: UpdateGraphInput, graph_uuid: uuid.UUID
    ) -> Graph:
        await graphql_check_authenticated(info)

        graph = await story_graph_models.Graph.objects.aget(uuid=graph_uuid)

        for key, value in graph_input.__dict__.items():
            if value == strawberry.UNSET:
                continue
            graph.__setattr__(key, value)

        await graph.asave()

        return graph  # type: ignore

    @strawberry.mutation
    async def add_audio_file(self, info, new_audio_file: AddAudioFile) -> AudioFileUploadResponse:  # type: ignore
        if new_audio_file.file is None or len(new_audio_file.file) == 0:
            return InvalidAudioFile(error="Received empty audio file")
        elif not os.path.splitext(new_audio_file.file_name)[-1].lower() in [
            ".flac",
            ".wav",
        ]:
            return InvalidAudioFile(error="Only support flac and wav files")
        try:
            audio_file = await stream_models.AudioFile.objects.acreate(
                name=new_audio_file.name,
                file=File(new_audio_file.file, name=new_audio_file.file_name),
                description=new_audio_file.description,
                auto_generated=False,
            )
        except Exception as e:
            return InvalidAudioFile(
                error=f"Unexpected error, could not save audio file: {e}"
            )
        return audio_file

    @strawberry.mutation
    async def create_update_stream_variable(
        self, info, stream_variables: List[StreamVariableInput]
    ) -> List[StreamVariable]:
        stream_vars: List[stream_models.StreamVariable] = []

        for stream_variable in stream_variables:
            (
                stream_var,
                _,
            ) = await stream_models.StreamVariable.objects.aupdate_or_create(
                stream=await stream_models.Stream.objects.aget(
                    uuid=stream_variable.stream_uuid
                ),
                key=stream_variable.key,
                defaults={
                    "value": stream_variable.value,
                    "stream_to_sc": stream_variable.stream_to_sc,
                },
            )
            if stream_variable.stream_to_sc:
                await sync_to_async(stream_var.send_to_sc)()
            stream_vars.append(stream_var)

        return stream_vars  # type: ignore

    @strawberry.mutation
    async def create_node_door(
        self,
        info,
        node_door_input: NodeDoorInputCreate,
        node_uuid: uuid.UUID,
    ) -> NodeDoor:
        await graphql_check_authenticated(info)
        node = await story_graph_models.Node.objects.aget(uuid=node_uuid)
        return await story_graph_models.NodeDoor.objects.acreate(
            door_type=node_door_input.door_type,
            node=node,
            name=node_door_input.name,
            order=node_door_input.order,
            code=node_door_input.code,
        )  # type: ignore

    @strawberry.mutation
    async def update_node_door(
        self,
        info,
        node_door_input: NodeDoorInputUpdate,
    ) -> NodeDoorResponse:  # type: ignore
        await graphql_check_authenticated(info)
        node_door = await story_graph_models.NodeDoor.objects.aget(
            uuid=node_door_input.uuid
        )
        node_door.door_type = node_door_input.door_type
        if node_door_input.code:
            node_door.code = node_door_input.code
        if node_door_input.name:
            node_door.name = node_door_input.name
        if node_door_input.order:
            node_door.order = node_door_input.order
        try:
            await node_door.asave()
        except SyntaxError as e:
            return InvalidPythonCode(
                error_type=e.msg,
                error_code=e.text if e.text else "",
                error_message=create_python_highlight_string(e),
            )
        return node_door  # type: ignore

    @strawberry.mutation
    async def delete_node_door(self, info, node_door_uuid: uuid.UUID) -> bool:
        """Allows to delete a non-default NodeDoor.
        If a node door was deleted it will return ``True``, otherwise ``False``.
        """
        await graphql_check_authenticated(info)
        deleted_objects, _ = await story_graph_models.NodeDoor.objects.filter(
            is_default=False,
            uuid=node_door_uuid,
        ).adelete()
        return deleted_objects >= 1


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def graph(
        self,
        info: Info,
        graph_uuid: uuid.UUID,
    ) -> AsyncGenerator[Graph, None]:
        """Used within the editor to synchronize any updates of the graph such as movement
        of a :class:`~story_graph.models.Node`.
        """
        graph = await story_graph_models.Graph.objects.aget(uuid=graph_uuid)
        yield graph  # type: ignore

        async for graph_update in GenCasterChannel.receive_graph_updates(
            info.context["ws"], graph_uuid
        ):
            yield await story_graph_models.Graph.objects.aget(uuid=graph_update.uuid)  # type: ignore

    @strawberry.subscription
    async def node(
        self,
        info: Info,
        node_uuid: uuid.UUID,
    ) -> AsyncGenerator[Node, None]:
        """Used within the editor to synchronize any updates on a node such as updates on a
        :class:`~story_graph.models.ScriptCell`.
        """
        node = await story_graph_models.Node.objects.aget(uuid=node_uuid)
        yield node  # type: ignore

        async for node_update in GenCasterChannel.receive_node_updates(
            info.context["ws"], node_uuid
        ):
            yield await story_graph_models.Node.objects.aget(uuid=node_update.uuid)  # type: ignore

    @strawberry.subscription
    async def stream_info(
        self,
        info: Info,
        graph_uuid: uuid.UUID,
    ) -> AsyncGenerator[StreamInfoResponse, None]:  # type: ignore
        """Used within the frontend to attach a user to a stream.
        :class:`~story_graph.engine.Engine` contains the specifics of how the iteration over a
        graph is handled.

        Upon visit the ``num_of_listeners`` of the associated
        :class:~stream.models.Stream` will be incremented which indicates
        if a given stream is free or used.
        Upon connection stop this will be decremented again.
        """
        consumer: GraphQLWSConsumerInjector = info.context["ws"]

        graph = await story_graph_models.Graph.objects.aget(uuid=graph_uuid)

        try:
            stream = await stream_models.Stream.objects.aget_free_stream(graph)
            log.info(f"Attached to stream {stream.uuid}")
        except NoStreamAvailableException:
            log.error(f"No stream is available for graph {graph.name}")
            yield NoStreamAvailable()
            return

        async def cleanup():
            await stream.decrement_num_listeners()

        async def cleanup_on_stop(**kwargs: Dict[str, str]):
            """
            A helper function which scans for a "stop" signal send via the websocket connection of our
            graphql subscription as this is the indication from urql that we paused the subscription.
            """
            if text_data := kwargs.get("text_data"):
                d = json.loads(text_data)  # type: ignore
                if d.get("type") == "stop":
                    log.info("Stop a stream due to a stop signal")
                    await cleanup()

        with db_logging.LogContext(db_logging.LogKeyEnum.STREAM, stream):
            engine = Engine(
                graph=graph,
                stream=stream,
            )

            await stream.increment_num_listeners()

            consumer.disconnect_callback = cleanup
            consumer.receive_callback = cleanup_on_stop

            # send a first stream info response so the front-end has
            # received information that streaming has/can be started,
            # see https://github.com/Gencaster/gencaster/issues/483
            # otherwise this can result in a dead end if we await
            # a stream variable which is set from the frontend
            yield StreamInfo(stream=stream, stream_instruction=None)  # type: ignore

            async for instruction in engine.start(max_steps=int(10e4)):
                if type(instruction) == Dialog:
                    yield instruction
                else:
                    yield StreamInfo(
                        stream=stream,  # type: ignore
                        stream_instruction=instruction,  # type: ignore
                    )
            yield GraphDeadEnd()

    @strawberry.subscription
    async def stream_logs(self, info: Info, stream_uuid: Optional[uuid.UUID] = None, stream_point_uuid: Optional[uuid.UUID] = None) -> AsyncGenerator[StreamLog, None]:  # type: ignore
        stream_logs = stream_models.StreamLog.objects.order_by("created_date")
        if stream_uuid:
            stream_logs = stream_logs.filter(stream__uuid=stream_uuid)
        if stream_point_uuid:
            stream_logs = stream_logs.filter(stream_point__uuid=stream_point_uuid)
        async for stream_log in stream_logs.all():
            yield stream_log  # type: ignore

        async for log_update in GenCasterChannel.receive_stream_log_updates(
            info.context["ws"],
        ):
            if stream_uuid:
                if str(log_update.stream_uuid) != str(stream_uuid):
                    continue
            if stream_point_uuid:
                if str(log_update.stream_point_uuid) != str(stream_point_uuid):
                    continue
            yield await stream_models.StreamLog.objects.aget(uuid=log_update.uuid)  # type: ignore

    @strawberry.subscription
    async def streams(self, info: Info, limit: int = 20) -> AsyncGenerator[List[Stream], None]:  # type: ignore
        async def get_streams() -> List[Stream]:
            # as slicing operation is not implemented in async mode we need this
            # helper function
            streams_db: List[Stream] = []
            async for stream in stream_models.Stream.objects.order_by("-created_date")[
                0:limit
            ]:
                streams_db.append(stream)  # type: ignore
            return streams_db

        yield await get_streams()

        async for _ in GenCasterChannel.receive_streams_updates(info.context["ws"]):
            yield await get_streams()


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
)
