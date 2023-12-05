Listening to a graph
====================

Building a story graph is one thing, but just as important is listening to the graph.
Gencaster provides a player for a story graph via a website, which makes it possible to distribute the content of the story graph to any internet-enabled device.

Gencaster can also manage not only one stream, but multiple streams at the same time, so that each listener gets their own stream.
This allows for example to create new ways of cheap and interactive spatial setups.

The frontend handles all necessary communication and streaming connection setup with the SuperCollider server using a technology called `WebRTC <https://webrtc.org/>`_.
This allows you to listen to a Gencaster stream in your browser without the need to install any application.

.. important::

  Due to `playback limitations <https://developer.mozilla.org/en-US/docs/Web/Media/Autoplay_guide>`_ within the browser, it is still necessary for the user to interact with the website, e.g. by clicking a button in order to start playback of the stream.

.. admonition:: Action

    * Visit the frontend with your web browser
    * In the list of all story graphs on the server, click on the one you just created
    * Click on *Start*. You should hear a high pitched percussive sound.
    * After around 20 seconds the screen will turn blank - we reached the end of the graph
      and an ending message will be displayed.
      As we have not defined it yet, it will be simply a blank screen.

      Note that although we hit the end of a graph, we still hear its sound.
      This is intentional as it allows for "never-ending" fade-outs.
    * Do the same on another device, e.g. your smartphone.
      Verify that both signals, although similar, are not the same.

Graph metadata
--------------

To give a graph some context, it is possible to specify an intro text that is displayed above the start button, an about text that is available while the graph is being listened to, and an end text that is displayed when the graph is *finished*.
A graph is *finished* when there are no nodes or script cells left to execute.

The content of these text fields is formatted using `Markdown <https://www.markdownguide.org/basic-syntax/>`_ which also allows you to display images - either by referencing their URL or by copying and pasting them into the text field (but please not too large images).

.. admonition:: Action

    * In the graph editor, click on the *Meta* tab in the upper left corner
    * Write something for the intro, about and end text
    * Afterwards click on *Save* in the upper right corner
