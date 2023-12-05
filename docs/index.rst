Gencaster
=========

Gencaster is a non-linear audio streaming framework for real-time radiophonic experiences and live music.

The audio streams created through Gencaster have a low latency (about 150ms) and can be listened to in any modern browser, and can dynamically render audio content based on a given story graph that can react to user input such as name, time, GPS position, or even microphone streaming after permissions have been granted.

Gencaster consists mainly ofthe following services.

* :ref:`Caster sound<caster-sound>` is a service that handles all streaming and audio rendering functionality, using SuperCollider to generate audio and Janus to distribute audio to listeners via WebRTC

* :ref:`The backend<caster-back>` manages the streams of caster-sound, written in Django.
  To communicate with :ref:`Caster sound<caster-sound>`, it uses the :ref:`OSC Server` service.

* :ref:`The frontend<caster-front>` allows users to listen to the streams of :ref:`Caster sound <caster-sound>` and acts as a player.
  It is written in Vue.

* :ref:`The editor <caster-editor>` is a website in which the actions of a stream, called a :term:`Story Graph`, can be created, edited and tweaked using Python or SuperCollider, and is also written in Vue.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :hidden:

   tutorial.rst
   services.rst
   deployment.rst
   glossary.rst
