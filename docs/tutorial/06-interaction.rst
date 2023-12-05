Listener interaction
====================

After introducing the SuperCollider, Audio and Markdown cells, it is now time to take a look at what a Python script cell can offer.
With Python script cells it is possible to

* Interact with the listener by requesting some input
* Generate or calculate some dynamic text
* Control what is displayed on the listener's screen
* request information from a database or the Internet, or
* navigate the user through several possible paths

This allows you to create more dynamic content within Gencaster, creating more of a dialog between the listener and the streamer.

.. _stream variable:

Stream variable
---------------

In order to respond to events or information from the user, it is necessary to have a way to pass information from the listener to the server that controls the sonic content of the stream.
To attach information to a running stream, a stream variable is used.
Each stream variable is stored as a string in the database under a *key*.
It is possible to access and set this variable from different script cells throughout the graph.

The native way of interacting and managing these streaming variables is through the Python script cells through the ``vars`` variable, which is a `dictionary <https://realpython.com/python-dicts/>`_ of all stream variables.
There are several triggers and helper functions built into Gencaster, such as :func:`~story_graph.engine.Engine.wait_for_stream_variable`, which allows to wait for example a certain event which has been triggered by the user.

In order to wait for the execution of the graph until a user presses the *Start* button in the frontend, it is possible to wait for the stream variable ``start`` which is set as soon as the listener presses the *Start* button.
This is a common pattern within Gencaster as due browser restrictions it is not possible to playback any sound before any button is pressed.
We can use a Python script cell to wait until this variable has been set by adding a Python script cell to a given node with the following code.

.. code:: python

    await wait_for_stream_variable("start")


.. admonition:: Action

    * Also wait for the press of *Start* from the user before playing any sound.
      Note that it is possible to arrange the order of the script cells via drag and drop.

.. note::

    The code of a Python script cell is executed within an `async runtime  <https://realpython.com/async-io-python/>`_.
    Also, for security reasons, the modules and functions which one can use within a Python script cell is limited and are stated explicitly.
    The documentation and source code of :func:`~story_graph.engine.Engine.get_engine_global_vars` show all available functions and modules.


Triggering dialogs
------------------

Gencaster not only allows to communicate with the listener through the sonic stream but also through the display of the device.
Via a Python cell it is possible to construct a Dialog (e.g. its title, content and its button) and *yield* it to the frontend of the user.

.. code:: python

    yield Dialog(
        title="Hello World",
        content=[
            Text(text="I was triggered from within a Python cell."),
        ],
        buttons=[Button.ok()],
    )

.. admonition:: Action

    * Create a Python script cell in a node and paste the code above in it
    * Save the node and try it out in the frontend
    * Modify the text which should be displayed.
    * Note that during each call of the code a dialog will be put on the stack of dialogs which needs to be displayed on the frontend.


Storing user input in stream variables
--------------------------------------

While triggering a dialog on the listener's screen allows for more interaction with the listener and waiting for user-triggered events, it is also possible to use dialogs to retrieve text-based information from the listener and store that information in a stream variable.

The following code creates a dialog that displays a text box where the listener can enter a name.
The result is transferred and stored in a new stream variable called ``name`` and is available within Python.

.. code:: python

    yield Dialog(
        title="Who are you?",
        content=[
            Text(text="Can we ask for your name?"),
            # key will be used as the key for the stream variable name
            Input(label="Name", key="name"),
        ],
        buttons=[Button.cancel(), Button.ok()],
    )

In order to use this variable within a Markdown/text-to-speech context, it is possible to access the stream variables via the ``var`` statement within a Markdown script cell.

.. code:: markdown

    Hello {var}`name`.

If the listener stated *Italo* as a name, the listener will hear *Hello Italo* on the stream.
There are also built in dialogs such as requesting the GPS address of the user, which are documented in :ref:`the python script cell documentation of the editor<editor_python>`.

.. admonition:: Action

    * Create a dialog which asks for a favorite pet - or something else, and store it in
    * Wait for the user input.
    * Use the pet within a Markdown cell.


Conditional dialogs
-------------------

Creating endless or repeating (sub-)cycles within the story graph is a common pattern within Gencaster, but this can conflict with user information we want to ask only once.
To ask for a name only once, it is possible to wrap the output of a dialog in an if condition, which checks if a stream variable for a certain key has already been set using the ``vars`` dictionary.

.. code-block:: python

    if vars.get("name") is None:
        yield Dialog(
            title="Who are you?",
            content=[
                Text(text="Can we ask for your name?"),
                # key will be used as the key for the stream variable name
                Input(label="Name", key="name"),
            ],
            buttons=[Button.cancel(), Button.ok()],
        )
        await wait_for_stream_variable("name")

Creating streaming variables
----------------------------

We can also store the number of visits of a script cell, using the `*walrus operator* <https://docs.python.org/3/whatsnew/3.8.html#assignment-expressions>`_.
Assigning a stream variable is as easy as declaring a new key for the ``vars`` variable.

.. code-block:: python

    if counter:=vars.get("counter"):
        # streaming variables are always strings
        # therefore we need to cast them e.g. to strings
        counter = int(counter)+1
    else:
        vars["counter"] = 1


.. note::

    The SuperCollider and the Python script cell don't only serve different purposes, they also behave differently.
    A Python script cell always starts *from scratch*, so functions declared in another script cell that may have already been evaluated are not available for execution.

    On the other hand, SuperCollider script cells are executed in the context of the previous state of the SuperCollider interpreter - so variables and functions declared earlier are also available in the context of the script cell.
