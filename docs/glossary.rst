Glossary
========

.. glossary::

    Backend

        See :term:`Services`.

    Django

        `Django <https://www.djangoproject.com/>`_ is used as the web server framework for Gencaster.
        For example, it manages the database and wraps the :term:`Engine` into a :term:`GraphQL` connection.

    Docker

        Docker is a virtualization software which allows to specify the runtime of a service through code.
        This helps to make the installation, deployment and management of Gencaster easier.

    Edge
    Connection

        Connects an entry :term:`node door<Node door>` with an exit node door.

        See :class:`story_graph.models.Edge`.

    Editor

        See :term:`Services`.

    Engine

        The story graph engine traverses the :term:`Story Graph` and manages any script cell executions and allocations.

        See :class:`story_graph.engine.Engine`.

    Frontend

        See :term:`Services`.

    Graph
    Story Graph

        A graph is a key component of Gencaster and is used to define the score of a story within Gencaster.
        A graph stores the content, metadata and code statements which will control and influence the stream of the listener.
        Each Graph consists of multiple :term:`nodes <Node>` which are connected through :term:`edges<Edge>`.

        See :class:`story_graph.models.Graph`.

    GraphQL

        GraphQL has nothing to do with :term:`Story Graph`, but instead is a communication protocol used between :term:`Frontend` and :term:`Backend`.

        See :ref:`schema`.

    Janus

        The WebRTC server used to distribute/broadcast the sonic output of :term:`scsynth` via :term:`WebRTC`.

    Node

        A node is an entity within the :term:`Story Graph` and consists of any number of :term:`script cells<Script Cell>` as well as any number of :term:`node doors<Node door>`.

        See :class:`story_graph.models.Node`.

    Node door

        The entering and exiting of a :term:`node <Node>` is managed through *node doors*.
        Each node has at least an default exit door, but can also have multiple exit nodes.
        Additionally, each node also has an entry door which enforces the flow such that an *exit* door can be only connected to an *input* door of a node.

        Also see :ref:`the node door tutorial<tutorial_node_door>` for further information.

        See :class:`story_graph.models.NodeDoor`.

    Pipewire

        Used as a replacement for Jack within Gencaster, which manages the *piping* of the :term:`scsynth` output to :term:`Janus`.
        Gencaster used to rely on Jack but the virtualization performance was very bad, which Pipewire fixed.

    Services

        See :ref:`services`.

    Script cell

        A script cell wrap code statements, see :ref:`tutorial_script_cell`.

        See :class:`story_graph.models.ScriptCell`.

    sclang

        *sclang* is the programming language of the SuperCollider framework.
        Within Gencaster it is used to control the content of the stream.

    scsynth

        scsyth is the synthesis enginge of SuperCollider and is responsible to generate sounds on the Gencaster stream.

    Stream

        A stream combines a listener with a :term:`Stream Point` and a :term:`Story Graph`.
        There can be multiple listeners on a stream, determined by the :term:`Stream Assignment Policy`.
        If the listener count becomes 0, the stream will be closed and the stream point will be available for the next listener.

        See :class:`stream.models.Stream`.

    Stream Assignment Policy

        See :class:`story_graph.models.Graph.StreamAssignmentPolicy`.

    Stream Point
    Streaming Point


        A stream point encapsules a combination of a :term:`Janus` `stream <https://janus.conf.meetecho.com/docs/streaming.html>`_, optional `audio bridge <https://janus.conf.meetecho.com/docs/audiobridge.html>`_ and a :term:`scsynth` instance.
        Gencaster can only manage as many parallel streams as there are stream points available.

        See :class:`stream.models.StreamPoint`.

    Stream Variable

        Stream variable allow to attach information on a :term:`stream<Stream>`.

        See :class:`stream.models.StreamVariable`.

        .. important::

            A stream variable is **always** a string.
            Even if a stream variable has been set to a number or boolean value through a Python cell, the stream variable will be a string in the next script cell.

    SuperCollider

        SuperCollider is a framework for algorithmic composition and beyond.
        Gencaster uses :term:`scsynth` and :term:`sclang` in order to create sounds on the stream.

    Vue

        `Vue <https://vuejs.org/>`_ is a JavaScript framework which is used to build to :term:`Frontend` and the :term:`Editor`.

    WebRTC

        WebRTC is the streaming technology which is used by Gencaster.
        It is supported by all major browsers and allows to distribute media in real time and in high quality.
        The actually used WebRTC server is `Janus <https://janus.conf.meetecho.com/>`_.
