.. _Story Graph:

The story graph
===============

The story graph acts as a central element of Gencaster to create and control the non-linear storytelling experiences of Gencaster.
It creates and negates possibilities through connections and statements within this graph.

A Gencaster instance can store multiple graphs that are shared and identified by a name and a URL that can be used for listening or editing.
When a user visits the URL of a story graph, a stream is assigned to the user and connected to the user.

The graph itself consists of *nodes* connected by *connections* (or *edges*) and metadata such as a name for the graph.
You can think of a graph as a web on which the listener lives and navigates.
How this web looks like and what actions can happen is up to the author.
The theoretical concept behind the story graph is motivated by a `*finite state machine* <https://www.youtube.com/watch?v=vhiiia1_hC4>`_, which defines all possible transitions between all possible states and is often used to model event-driven processes, allowing a clear visual representation of a complex system.

.. admonition:: Action

    * Visit the editor in your web browser
    * Login with your credentials - you will be redirected to the list of all graphs of the Gencaster instance.
    * Create a new graph by scrolling down the list of all existing graphs and clicking on the `+` symbol.
      You will be asked for a name for the graph and after clicking *OK* you will be redirected to the new graph.

Node
----

Each story graph consists of at least one *node*, the *start node*, which is used as the entry node for the listener.
Upon connection, the user starts the journey on the graph with this node by executing its content.

.. graphviz::
    :caption: A story graph at least consists of a start node

    digraph StoryGraph {
        node [fontname="Arial"]
        "Start" [fillcolor=lightgray style=filled];
    }

The content of each node consists of one or more *script cells* that control the actions on a stream.
The order of the script cells is deterministic because they are ordered in a list.

.. _tutorial_script_cell:

Script cell
-----------

There are several types of script cells, each serving a different purpose by having a different handle on possible events.

.. list-table:: Script cell types
    :header-rows: 1
    :widths: 15 30

    * - Script cell type
      - Comment
    * - Markdown
      - Markdown is a markup language used in Gencaster to speak on the stream.
        A text-to-speech engine is used to convert the written text into spoken text.
        There are several ways to dynamically control the content of the speech as well as the voice that speaks it.
    * - Audio
      - An audio cell is always associated with an audio file that is used for playback in the stream that can be uploaded through a dialog of the editor.
        There are several ways to play the file, such as continuing to play in the background, or waiting for the file to finish playing before continuing with another action.
    * - Python
      - Python is a scripting language and can be used to implement custom logic or data retrieval.
        It is also used to trigger dialogs for the listener, calculate and store information, access data from the internet or control the movement within the graph.

        In fact, a large part of Gencaster is built with Python and every other cell is based on a Python cell in the Python cell in the background.
    * - SuperCollider
      - SuperCollider is used for the synthesis of sounds within Gencaster.
        Via *sclang*, the scripting language of SuperCollider, commands can be executed within the sound generating server *scsynth*.

        SuperCollider has many different kind of dialects (different ways of achieving the same results but with different tools or best practices), but Gencaster advocates the `JITLib <https://docs.supercollider.online/Classes/Ndef.html>`_ dialect.
    * - Comment
      - The comment cell is simply a way to annotate things without affecting the actions of a cell. It is more useful than it may sound at first.

To summarize, a *node* is simply a collection of statements which are represented by *script cells*.


.. admonition:: Action

    * Double click on the start node - this will open the editor for the node in which you can
      edit the content of the script cells - but currently this will be empty.
    * Create a SuperCollider script cell and copy the following code into it.
      If you are already familiar with SuperCollider you can also adjust the code to your liking

      .. code:: supercollider

        // clear any running sounds
        Ndef.clear;

        Ndef(\helloGencaster, {
            // create a basic signal - a phase modulated sine oscillator
            var sig = SinOsc.ar(
                freq: LFDNoise0.kr(4.0!2).exprange(1000, 14000),
                phase: SinOsc.ar(LFDNoise0.kr(0.5!2).exprange(10, 10000)).lag(0.5),
            );
            // create an amplitude envelope
            var env = EnvGen.kr(
                envelope: Env.perc(releaseTime: 0.1),
                gate: Impulse.kr(8.0!2, phase: [0, pi]) + Dust.kr(4.0!2),
            );
            // a feedback signal
            var oldSig = LocalIn.ar(2);
            // randomly select between feedback and feedforward signal
            sig = SelectX.ar(LFDNoise3.kr(4.0!2).range(0, 1), [sig, oldSig]);
            // apply some pitch shifting and delay on the feedback signal
            LocalOut.ar(
                channelsArray: PitchShift.ar(
                    in: CombC.ar(
                        in: sig,
                        decaytime: 0.2,
                    ),
                    windowSize: 0.4,
                    pitchRatio: LFDNoise0.kr(10.2!2).range(0.25, 4),
                    timeDispersion: 0.5,
                )
            );
            // put sig and amp envelope together
            sig = sig * env * \amp.kr(0.4);
            sig.tanh;
        }).play;

        // we need to wait here because otherwise the
        // graph is finished directly at the beginning
        20.0.wait;

    * Click *Save node* in the upper right corner in order to transmit the
      content of the script cell to the server.

    .. important::

        It is not necessary to wrap the SuperCollider code into brackets ``()`` as each script cell will be automatically wrapped in it.
