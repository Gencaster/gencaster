Live editing
============

The relationship between the Gencaster editor and its player is much more direct than you might think at first.
When a listener visits a graph via the frontend, Gencaster connects the listener to a stream and starts traversing the graph with the listener.

But the graph can be changed while the listener is traversing it - this includes the topology of the graph as well as the statements within the script cells.
So it is possible to add or delete new connections while the user is traversing the graph.
All decisions are made as late as possible, so Gencaster only looks at all available outputs of a node when a node needs to be exited.
The same applies to the code inside the script cells: The content of a script cell is only looked at when it is executed.

Since Gencaster allows many listeners to traverse the graph independently, this feature can also be used to synchronize all listeners on the same graph by simply leading all nodes to the same *pause node*, which simply collects all listeners on the graph and redirects them to another node for further action.

Of course, this also hopefully makes it easier to create a story graph, since you can listen to it as you create it.

.. admonition:: Action

    * Change the layout of the graph while listening to it.
      Creating a dead end will stop the execution of the graph when a listener visits it.
    * Change some parameters of the code while listening.
      Simply change some numbers within the SuperCollider code and press *Save node* while listening to the graph.
      You should be able to hear the updates the next time the script cell will be traversed.

Collaboration
-------------

The synchronization of the graph exists not only between the editor and the listener, but also between multiple instances of the editor.
Many people can edit and tweak the same graph through the editor, while their changes are synchronized by broadcasting them to everyone else.

This allows new ways of collaboration, since not only listening to the graph is distributed, but also editing the graph.
There can be :math:`n` listeners and :math:`m` editors on the same graph, interacting via sound or code.
Of course, the set of listeners and editors can overlap, creating new possibilities for distributed live coding.

.. admonition:: Action

    * Open a second browser window and visit the graph editor
    * Tweak the node in one of the graph editor windows and verify that the tweaks will be also synchronized with the other window.
      The other window can also be on another computer.

.. todo::

    The synchronization of the script cell content with other editors does currently not work.
