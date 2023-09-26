.. _Story Graph:

Story Graph
===========

.. contents:: :local:
    :depth: 2


.. seealso::

    This documents covers the concept behind a story graph.
    The editing of such a graph can be found in :ref:`caster-editor`.


The story graph acts as a central element of Gencaster to create non-linear storytelling experiences.
In non-linearity the concept of a timeline is replaced by a tree of possibilities that the listener walks along.
A story graph allows to construct such possibilities which cover

* the playback of audio files
* generating speech to text
* triggering input dialogs

and much more.

Node
----

A *Node* represents a group of statements which will be executed for the listener upon visiting said node.
Each node contains one or multiple *script cells*, which are described further at :ref:`editor script cells`.

Each session of a listener starts on the *Start node*.

.. graphviz::
    :caption: A story graph at least consists of a start node

    digraph StoryGraph {
        "Start";
    }


Edge
----

In order to jump from one node to another one it is necessary to connect these two with an *edge*.
This *edge* is directed, which means that the edge works only in one direction, from an outgoing *start node*
to an incoming *end node*.

.. graphviz::
    :caption: A connection between two nodes can be established via an edge.
        This connects the *Start* node to the *Play music* node.

    digraph StoryGraph {
        "Start" -> "Play music";
    }

.. todo::

    If multiple *outgoing* edges are present it is currently determined by chance which node
    will be taken.
    This is about to change and is WIP.

    .. graphviz::
        :caption: Multiple outgoing connections from the *Start node*.
            There is a 50/50 chance which following node will be selected.

            digraph StoryGraph {
                "Start" -> "Play music";
                "Start" -> "Play podcast";
            }

It is possible to create loops within the story graph.

.. graphviz::
    :caption: A graph which loops indefinitely.

    digraph StoryGraph {
        "Start" -> "Play music";
        "Play music" -> "Play podcast";
        "Play podcast" -> "Start";
    }

.. _Node Door:

Node Door
---------

For a more technical description of a Node Door see :class:`story_graph.models.NodeDoor`.

.. _Stream Variable:

Stream Variable
---------------

For a more technical description of a Stream Variable see :class:`stream.models.StreamVariable`.

.. _Graph Meta:

Graph Metadata
--------------

Stream assignment policy
^^^^^^^^^^^^^^^^^^^^^^^^

There are...
