.. _caster-editor:

Caster Editor
=============

.. contents:: :local:
    :depth: 2


.. seealso::

    This documents covers the editing of a *story graph*.
    For the concepts of such a graph see :ref:`Story Graph`.

The editor is a website which allows to create and modify a :ref:`Story Graph`.
It is possible that many users at once can collaboratively edit this story graph, and also the modifications will be applied in real time to an already running stream, which allows for live coding setups.

.. figure:: ./assets/editor.png
   :alt: A screenshot of the editor

   A screenshot of the editor which shows all the *nodes* of a story graph as well as their connections, called *edges*.
   If a node is double clicked, the node editor will be opened (right side) which shows the :ref:`editor script cells` and :ref:`editor node doors` of the node,
   whose content can be edited here.

.. _editor script cells:

Script cells
------------

Script cells contain different kind of instructions which control what happens on the stream or the story graph.
There are multiple types of script cells for different contexts.

.. list-table:: Script cells
   :widths: 10 30
   :header-rows: 1

   * - Script cell type
     - Description
   * - Markdown
     - Write text which will be transferred to a spoken text via a Text to Speech engine.
       The text can also be variable by using the value of a :ref:`Stream Variable`.
   * - Audio
     - Provides an interface to upload prepared audio files so that they can be played back on the stream.
   * - SuperCollider
     - SuperColider is a framework for audio engine and Gencaster uses it to generate the audio stream.=
       It also contains the scripting language *sclang* which allows to adjust the auditory content on the stream.
   * - Python
     - Python is a scripting language which allows to modify and interact with the story graph and also trigger
       e.g. PopUps on the :ref:`caster-front`.
       Anything that should be decided dynamically (e.g. day vs night) should be coded within Python.

Markdown
^^^^^^^^

Markdown is a way to write formatted text in an easy but extensible manner.
The written text will be converted to audio via :class:`~stream.models.TextToSpeech`.

It is possible to make this text dynamic by using the value of a :ref:`Stream Variable` within the text.

All custom Gencaster markdown macros are documented in :class:`~story_graph.markdown_parser.GencasterRenderer`.

Examples
""""""""

**Speak a text on the stream**

By creating a markdown script cell and enter the text

.. code-block:: markdown

    Ich wünsch einen schönen Tag.

the text *Ich wünsche einen schönen Tag* will be spoken on the stream.

**Add a break between words**

.. code-block:: markdown

    Hallo {break}`300ms` dort.

**Switch between voices**

There is a variety of voces to choose from, which are documented in :class:`stream.models.TextToSpeech.VoiceNameChoices`.

The default voice is ``DE_NEURAL2_C__FEMALE``, but if we want to switch temporary to e.g. a male voice it is possible via

.. code-block:: markdown

    This is me and {male}`this is also another me`.

.. todo::

    Switch between multiple speakers by their name.


**Use the name of the user**

First it is necessary to trigger a popup in the frontend so that the user can enter their name.
This is handled via a Python script cell, see :ref:`trigger a popup via a python script cell <python ask name>` which stores the name under the :ref:`Stream Variable` ``name``.

To use this ``name`` within a Markdown cell can be archived via


.. code-block:: markdown

    Hello ${var}`name`. I hope you are doing fine.

where the *${var}`name* will be replaced with the name provided through the popup, so for example *Hello Alice. I hope you are doing fine*.


Audio
^^^^^

An audio cell allows to playback a :class:`~stream.models.AudioFile` on the stream in two ways

- ``async`` will playback in the background and the story graph will continue with the execution
- ``sync`` will pause the execution of the story graph until the file has been played back fully.

The *volume* slider controls the volume of the audio on the stream.

The *edit* button allows to change the associated audio file by uploading a new file or search through existing files.

Python
^^^^^^

Python is an universal scripting language and allows to

- interact with the graph (e.g. set next node)
- assign or access a :ref:`Stream Variable`
- trigger dialogs on the frontend

Examples
""""""""

**Wait until user clicks on "Start" button**

When a user visits the story graph via the :ref:`Frontend <caster-front>` a first popup will be displayed which asks if the user wants to start streaming audio.
This is necessary due to `Autoplay restrictions in browsers <https://developer.mozilla.org/en-US/docs/Web/Media/Autoplay_guide>`_ which require a user interaction to playback any audio.

So in order to wait until the user hears audio (which will happen after the user clicks on start) the following snippet can be used.

.. code-block:: python

    await wait_for_stream_variable('start')

The execution is async which allows to wait for something to happen, for example waiting for a :ref:`Stream Variable` like in this case.
For more technical details see :meth:`~story_graph.engine.Engine.wait_for_stream_variable`.

**Access a stream variable**

A :ref:`Stream Variable` can be accessed through the ``vars`` dictionary.

.. code-block:: python

    # will return None if not set
    name = vars.get('name')

**Set a stream variable**

Assigning a :ref:`Stream Variable` to a value is possible by using the ``vars`` dictionary

.. code-block:: python

    vars['is_day'] = 8 < datetime.now().hour < 20

.. important::

    Although this statements results in a boolean value, a stream variable can only represent a string as it gets shared with many languages.

.. _python ask name:

**Create popup which asks for the name**

To trigger a dialog in the frontend use the ``yield`` command with a :class:`~stream.frontend_types.Dialog` instance.
The exact arguments are documented in :ref:`frontend-types`.

.. code-block:: python

    yield Dialog(
        title="Headline",
        content=[
            Text(text="Can we ask for your name?"),
            Input(label="Name", key="name"),
        ],
        buttons=[Button.cancel(), Button.ok()],
    )
    # wait for user input
    await wait_for_stream_variable("name")

This will save the value that was inserted by the user into tho variable ``name``.

.. figure:: ./assets/front-popup.png
   :alt: Popup in the front end which asks for the name of the user.
   :scale: 50%

   The code above generates a pop up where the user is asked for his name.
   The reply from the user is stored in the stream variable ``name``.


SuperCollider
^^^^^^^^^^^^^

A SuperCollider cell allows to directly control what happens in the audio domain of the stream.
The language used for this is *sclang* and the dialect of choice is the `*JITlib* dialect <https://doc.sccode.org/Overviews/JITLib.html>`_, although any other style is also possible, but may require more management.

Although *sclang* is a non-blocking language, it is possible to ``wait`` within a Script Cell and it is the easiest way to wait some time.

**Wait 10 seconds**

The following snippet will fade in over 10 seconds and after this will fade out within 1 second.

.. code-block:: supercollider

    Ndef(\drone, {
        SinOsc.ar(LFDNoise1.kr(0.1!2).exprange(100, 400)) * \amp.kr(0.2);
    }).fadeTime_(10.0).play;
    10.0.wait;
    Ndef(\drone).stop(fadeTime: 1.0);


Comment
^^^^^^^

A comment will be ignored for execution, but allows to add commentary on a node.

.. _editor node doors:

Node doors
----------


Meta
----


Debug Streams
-------------
