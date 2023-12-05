.. _tutorial:

Tutorial
========

..

    Der Rundfunk ist aus einem Distributionsapparat in einen Kommunikationsapparat zu verwandeln. Der Rundfunk wäre der denkbar großartigste Kommunikationsapparat des öffentlichen Lebens, ein ungeheures Kanalsystem, das heißt, er wäre es, wenn er es verstünde, nicht nur auszusenden, sondern auch zu empfangen, also den Zuhörer nicht nur hören, sondern auch sprechen zu machen und ihn nicht zu isolieren, sondern ihn auch in Beziehung zu setzen.

    -- Berthold Brecht

.. toctree::
   :maxdepth: 1
   :glob:
   :hidden:

   tutorial/*


Before explaining *how* Gencaster works, it might be useful to talk about the motivation behind Gencaster.
The main idea behind Gencaster is to enrich the techniques of dynamic broadcasting by creating a framework for interactive audio streams, aiming to overcome the limitations of cueing a set of static sound files within the browser and instead provide a flexible setup that can be used in a variety of use cases and opening new sonic possibilities.

Having previously worked on pieces that are driven by an interactive and dynamic rendering of sound (see `Social Score <https://socialscore.eu/>`_ or `Future Voices <https://futurevoices.radio/>`_), we wanted to build a framework that allows abstracting the building blocks of such broadcasting systems, inviting others to create pieces that rely on interaction through real-time information retrieval and dynamic response to it, without diving into the mechanics of setting up an audio stream environment.
Gencaster is therefore a framework, but also a platform, since it is possible to use existing Gencaster instances or to set up your own.

While *Social Score* already reacts to its environment in real time, it relies on two things we wanted to improve with Gencaster

* All possible (inter)actions are stored in a single JSON file, which makes it easy to bundle for the user, but difficult to edit and build.
* While the sound files were generated on the fly, they were sequenced through the browser, which limited its sonic compositing and reaction

The first problem was solved by thinking about ways to construct possible paths, something common in programming.
But instead of requiring people to *code* their possible stories, we wanted also people without programming skills to be able to use the framework, so we decided to build an editor that allows to create and edit a *story graph*, a key concept of Gencaster that will be discussed in the first chapter of the tutorial.
A key element of a story graph is that it can lay out a possible path while still allowing for wildcards within that path, allowing for a dialog between sender and receiver.

To improve the audio playback capabilities, we decided to abandon the Web Audio API of a browser and instead rely on the sonic capabilities of `SuperCollider <https://supercollider.github.io/>`_ which runs on a server and streams its output to the listener via WebRTC, which allows streaming media with high quality and low latency without the need for apps, simply relying on the capabilities of a smartphone browser.

Gencaster therefore takes care of what a user will hear according to the *score* of the story graph, and takes care of any necessary communication.

The presentation of the starting point and the direction of travel for Gencaster has hopefully provided a better understanding of what Gencaster wants to be: a platform for reactive audio content.

.. note::

   The tutorial tries to explain the basic concepts of Gencaster while giving some instructions and exercises to implement within Gencaster.
   The instructions and exercises are wrapped in a layout box - make sure you deviate from it to experiment a bit and get familiar with it by stepping into the un-pathed territory.

   Therefore, the tutorial assumes that you have access to a Gencaster instance to experiment with the examples.
   If this is not the case, you can contact the Gencaster team to get access to an instance or simply deploy your own instance, see :ref:`deployment`.
