Debugging
=========

After the tutorial introduced the major features of Gencaster, a last step is still missing which is how to figure what goes wrong in case something does not work as expected.

Listening to a stream without attaching to a graph
--------------------------------------------------

In order to verify that streaming works or attach oneself to a running stream without triggering the execution of the story graph, it is possible to use the debug website of the frontend, which is available for example under `dev.gencaster/debug <https://dev.gencaster.org/debug>`_.

Select the desired streaming point and use the player to tune into the stream.


Debugging the graph execution
-----------------------------

To verify the graph execution, the editor provides a list of current and past streams via `editor.dev.gencaster.org/stream <https://editor.dev.gencaster.org/stream>`_.
By clicking on a stream, the logs for the stream will be displayed and updating in real time.

Admin view
----------

There also exists a backend admin menu under `backend.dev.gencaster.org/admin <https://backend.dev.gencaster.org/admin/>`_ which can be used to verify the data stored within the database.
