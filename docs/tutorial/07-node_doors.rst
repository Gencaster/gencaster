.. _tutorial_node_door:

Node doors
==========

Until now, a listener's journey through a graph was either static (if each node of the graph had less than one successor node) or aleatory (if at least one node was connected to multiple successors).
But Gencaster also allows to control the navigation through a story graph based on conditional Python statements that specify which successor node should be selected.
This principle is called *node doors* in Python.

Like each graph has at least one node, the start node, each node has at least one node door, called the default node door.
In addition, each node has an *entry door* - this is the circle on the left side of each node, and for this document it is labeled as *Input* within the graphics.

Default node door
-----------------

On closer inspection of the nodes, the most simple connection looks like the following graph.

.. graphviz::
    :caption: The most basic connection - the *default* exit node door of the *Start* node is connected with the *input* door of *Other node*.

        digraph StoryGraph {
            subgraph cluster_0 {
                style=filled;
                color=lightgrey;
                node [style=filled,color=white, shape=box, fontname="Arial"];
                "startInput" [color=grey, label="Input"];
                "startDefault" [label="default"];
                "startInput" -> "startDefault";
                label = "Start";
            }
            subgraph cluster_1 {
                style=filled;
                color=lightgrey;
                node [style=filled,color=white, shape=box, fontname="Arial"];
                "mondayInput" [color=grey, label="Input"];
                "mondayDefault" [label="default"]
                "mondayInput" -> "mondayDefault"
                label = "Other node";
            }

            startDefault -> mondayInput;
        }

An exit door can also be connected to multiple input node doors, in which case the next node is chosen randomly.

.. graphviz::
    :caption: Randomly select the next node when multiple nodes are connected to the same node door

        digraph StoryGraph {
            edge [fontname="Arial"]
            subgraph cluster_0 {
                style=filled;
                color=lightgrey;
                node [style=filled,color=white, shape=box, fontname="Arial"];
                "startInput" [color=grey, label="Input"];
                "startDefault" [label="default"];
                "startInput" -> "startDefault";
                label = "Start";
            }
            subgraph cluster_1 {
                style=filled;
                color=lightgrey;
                node [style=filled,color=white, shape=box, fontname="Arial"];
                "mondayInput" [color=grey, label="Input"];
                "mondayDefault" [label="default"]
                "mondayInput" -> "mondayDefault"
                label = "Other Node";
            }
            subgraph cluster_2 {
                style=filled;
                color=lightgrey;
                node [style=filled,color=white, shape=box, fontname="Arial"];
                "otherDayInput" [color=grey, label="Input"];
                "otherDayDefault" [label="default"];
                "otherDayInput" -> "otherDayDefault";
                label = "Another node";
            }

            startDefault -> mondayInput [xlabel="50%"];

            startDefault -> otherDayInput [label="50%"];

        }


Additional node doors
---------------------

While the default node door does not check for any conditions, it is possible to add additional node doors to a node that will only be taken if a particular condition is met.
If none of the criteria of the additional node doors is met, the default node door is taken as the fallback exit.

The criteria can be a Python statement and has access.
It should return a statement which can be evaluated to ``True`` or ``False``.
If a criteria is too complex to be expressed within a single line of code, the value of the statement can be calculated in a Python script cell and stored within a stream variable.

.. graphviz::
    :caption: A graph which only enters the *monday* node if it is actually monday

    digraph StoryGraph {
        edge [fontname="Arial"]
        subgraph cluster_0 {
            style=filled;
            color=lightgrey;
            node [style=filled,color=white, shape=box, fontname="Arial"];
            "startInput" [color=grey, label="Input"];
            "startDefault" [label="default"];
            "startIsMonday" [label="isMonday"];
            "startInput" -> "startDefault";
            "startInput" -> "startIsMonday"
            label = "Start";
        }
        subgraph cluster_1 {
            style=filled;
            color=lightgrey;
            node [style=filled,color=white, shape=box, fontname="Arial"];
            "mondayInput" [color=grey, label="Input"];
            "mondayDefault" [label="default"]
            "mondayInput" -> "mondayDefault"
            label = "Monday";
        }
        subgraph cluster_2 {
            style=filled;
            color=lightgrey;
            node [style=filled,color=white, shape=box, fontname="Arial"];
            "otherDayInput" [color=grey, label="Input"];
            "otherDayDefault" [label="default"];
            "otherDayInput" -> "otherDayDefault";
            label = "otherDay";
        }

        startIsMonday -> mondayInput [label="today == 'monday'"];

        startDefault -> otherDayInput;

        otherDayDefault -> startInput;

        mondayDefault -> startInput;
    }

Adding an additional Node Door to a node can be done using the Node Editor: Double click on a node and at the bottom of the appearing drawer there is a ``+`` sign under *Node Exit Doors* which allows to create additional node doors for this node.
It may be necessary to scroll down if the contents of the script cells are long.
Each node door consists of a name and a Python statement.
For example, the statement to check if today is Monday is :code:`datetime.now().weekday() == 0`.
The default node door is also listed there, but it cannot be edited.

When all script cells of a node have been executed, each condition of each node door is evaluated in the order of their appearance (so it is possible to drag & drop the order of the node doors).
As soon as one of the conditions is fulfilled, the door is taken as an exit, so the order of the node doors can be important.
If none of the conditions returns ``True``, the node is exited through the default door.

.. admonition:: Action

    * Implement a dialog which asks the user to input a number.
      If this number is bigger than 5 go to node *A*, else go to node *B*.

      .. important::

            Stream variables are stored as strings in the database.
            When using numeric features of a stream variable, cast it to ``float`` or ``int``.

    * What happens if the user does not input a number?
      Can you come up with a graph which ensures that the listener inputs a number?
