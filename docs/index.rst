.. GenCaster documentation master file, created by
   sphinx-quickstart on Thu Mar 24 23:51:39 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Gencaster
=========

Gencaster is a non-linear audio streaming framework for real-time radiophonic experiences and live music and consists of multiple services.

The audio streams have a low latency (about 150ms) and can be listened to in any modern browser, and can dynamically render audio content based on a given story graph that can react to user input such as name, time, GPS position, or even microphone streaming after permissions have been granted.

* :ref:`caster-sound` is a service that handles all streaming and audio rendering functionality, using SuperCollider to generate audio and Janus to distribute audio to listeners via WebRTC

* :ref:`caster-back` is a web backend to manage the streams of caster-sound, written in Django

* :ref:`caster-front` is a web frontend that allows users to listen to the streams of caster-sound, written in Vue

* :ref:`caster-editor` is a web-editor in which the actions of a stream, called a :ref:`story-graph`, can be created, edited and tweaked using Python or SuperCollider, and is also written in Vue

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart.rst
   story_graph.rst
   services.rst
   deployment.rst
