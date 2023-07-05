.. _caster-editor:

Caster Editor
=============

.. seealso::

    This documents covers the editing of a *story graph*.
    For the concepts of such a graph see :ref:`story-graph`.


.. _caster-editor-script-cells:

Script cells
------------

Markdown
^^^^^^^^

Markdown is a way to write formatted text in an easy but extensible manner.
The written text will be converted to audio via :class:`~stream.models.TextToSpeech`.

It is possible to make this text dynamic by using the value of a :class:`~stream.models.StreamVariable` within the text.

.. code-block:: markdown

    Hello ${var}`name`.
    I hope you are doing fine.

All possible macros are documented in :class:`~story_graph.markdown_parser.GencasterRenderer`.

Audio
^^^^^

An audio cell allows to playback a :class:`~stream.models.AudioFile` on the stream in two ways

- ``async`` will playback in the background and the story graph will continue with the execution
- ``sync`` will pause the execution of the story graph until the file has been played back fully.


Python
^^^^^^

Python is an universal scripting language and allows to

- interact with the graph (e.g. set next node)
- create or read out :class:`~stream.models.StreamVariable`
- trigger dialogs on the frontend

The execution is async which allows to wait for something to happen, e.g. for a stream variable through an user interaction with the help of :meth:`~story_graph.engine.Engine.wait_for_stream_variable`.

.. code-block:: python

    await wait_for_stream_variable('start')

A stream variable can be accessed through a dictionary

.. code-block:: python

    # will return None if not set
    name = vars.get('name')

In order to set a stream variable, simply set the value in the ``vars`` dictionary

.. code-block:: python

    vars['day'] = 8 < datetime.now().hour < 20

To trigger a dialog in the frontend use the ``yield`` command with a :class:`~stream.frontend_types.Dialog` instance.
The exact arguments are documented in :ref:`frontend-types`.

.. code-block:: python

    yield Dialog(
        title="Headline",
        content=[
            Text("Can we ask for your name?"),
            Input(label="Name", key="name"),
        ],
        buttons=[Button.cancel(), Button.ok()],
    )
    # wait for user input
    await wait_for_stream_variable("name")

This will save the value that was inserted by the user into tho variable ``name``.


SuperCollider
^^^^^^^^^^^^^

A SuperCollider cell allows to directly control what happens in the audio domain of the stream.
The language used for this is *sclang* and the dialect of choice is the *JITlib* dialect.

The code can be async and will be handled in blocking manner which allows to wait on the stream, e.g. for a fade-in to finish.

.. code-block:: supercollider

    Ndef(\drone, {
        SinOsc.ar(LFDNoise1.kr(0.1!2).exprange(100, 400)) * \amp.kr(0.2);
    }).fadeTime_(10.0).play;
    10.0.wait;

.. important::

    Do not execute ``Tdef.clear`` as this will remove the beacon of the server and
    the stream will be considered offline from there on.


Comment
^^^^^^^

A comment will be ignored for execution, but allows to add commentary on a node.
