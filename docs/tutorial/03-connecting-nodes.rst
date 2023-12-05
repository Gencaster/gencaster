Connecting nodes
================

A single node in the graph will only get you so far.
Although the sound is modulated, it sounds rather static over time, so it should change over time.
SuperCollider implements several ways to sequence or modulate sounds over time (see e.g. `Tdef <https://docs.supercollider.online/Classes/Tdef.html>`_), but Gencaster also provides its own native way which aims more at an interaction between the listener, the stream and the database, represented by the graph already described.
A key aspect of a graph is not only its nodes, but much more the connection between the nodes, which is represented by *edges*.

Edge
----

In order to jump from a node :math:`A` to another node :math:`B`, it is necessary to connect these two nodes with an *edge*.
An edge in Gencaster is *directed*, which means that the edge only provides a way from node :math:`A` to node :math:`B`, but not the other way around (unless there is an additional edge that goes from :math:`B` to :math:`A`).

.. graphviz::
    :caption: A connection between two nodes can be established via an edge.
        This connects the *Start* node to the *Stop music* node.

    digraph StoryGraph {
        node [fontname="Arial"]
        "Start" [fillcolor=lightgray style=filled];
        "Start" -> "Stop music";
    }

A graph can contain an arbitrary number of nodes and edges, which allows complex structures to be built, and it is also allowed to build a graph that simply repeats itself, creating a loop by connecting a node to itself through another node.

.. graphviz::
    :caption: A graph which loops indefinitely.

    digraph StoryGraph {
        node [fontname="Arial"]
        "Start" [fillcolor=lightgray style=filled];
        "Start" -> "Stop music";
        "Stop music" -> "Start";
    }


.. admonition:: Action

    * In the build tab of the graph editor, create an additional node by clicking on *Add Node* on the upper left.
      Give the new node a name, for example *Stop music*
    * You can drag and drop the newly created node to a new position on the canvas with your mouse
    * Double click on the new node to open the node editor of it
    * Insert a SuperCollider cell with the following code (or something else)

      .. code:: supercollider

        Ndef.clear(fadeTime: 4.0);
        // wait for fade
        5.0.wait;

    * Create an edge between the *Start* node and the new node by hovering the mouse
      over the right *"circle"* on the Start node and drag the mouse pointer to the left
      circle of the new node and release the mouse button.
    * Do the same to create a connection from the new node to the start node.
      Your graph should look a bit like the graphic above.
    * Visit the frontend/player and listen what happens.
    * Notice that the ending screen does not appear anymore as we now traverse the graph
      indefinitely.

Creating multiple paths
-----------------------

Having only one way to walk a path on a graph is not the most interesting, as it could also be represented by a single script cell inside a node.
But Gencaster also allows to create more than one input and output edge on a node.
If a node has multiple outgoing edges, a random edge will be chosen to traverse.

.. graphviz::
    :caption: Multiple outgoing connections from the *Start node*.
        There is a 50/50 chance which following node will be selected.

        digraph StoryGraph {
            node [fontname="Arial"]
            "Start" [fillcolor=lightgray style=filled];
            "Start" -> "Play music";
            "Start" -> "Play podcast";
        }

.. admonition:: Action

    * Create another node, name it for example *Play other music*
    * Double click on the node to open its editor and insert a new SuperCollider
      script cell into it with the following code (or something else)

      .. code:: supercollider

        Ndef(\someOtherSound, {
            var baseFreq = LFDNoise0.kr(0.5).exprange(100, 200);
            var sig = 16.collect({|i|
                VarSaw.ar(
                    freq: (i*baseFreq) + (LFDNoise3.kr(i)*i),
                    width: LFDNoise1.kr(i),
                ) * EnvGen.kr(Env.perc(0.1, 0.01), gate: Dust.kr(2.0))
            });
            sig = Splay.ar(sig);
            CombC.ar(sig, delaytime: LFDNoise0.kr(2.0).range(0.01, 0.02).lag(0.1), decaytime: 1.0) * \amp.kr(0.5);
        }).play(fadeTime: 4.0);

        // listen to it for 10 seconds
        10.0.wait;

      Remember to click *Save node*.
    * Connect the output of the *stop music* node with the new node
    * Connect the output of the new node with the input of *stop music*.
      It should look something like the following graphic

      .. graphviz::
            :caption: Multiple outgoing connections from the *Stop music* node.
                There is a 50/50 chance that the next node after *Stop music* is the
                *Start* node or the *Play other music* node.

                digraph StoryGraph {
                    node [fontname="Arial"]
                    "Start" [fillcolor=lightgray style=filled];
                    "Start" -> "Stop music";
                    "Stop music" -> "Start";
                    "Stop music" -> "Play other music";
                    "Play other music" -> "Stop music";
                }

    * Listen to the result
    * Create additional edges - for example from "Start" to the new node in order
      to allow for overlapping of sounds.
