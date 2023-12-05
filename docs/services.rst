.. _services:

Services
========

Gencaster consists of multiple services which cover various tasks around the concept of a :ref:`Story Graph`.

.. _caster-sound:
.. _caster-front:

.. list-table:: Services
   :header-rows: 1
   :widths: 10 30

   * - Name
     - Description
   * - Frontend
     - A Javascript frontend which is used to listen to a :term:`Stream`.
       The frontend receives the data from the backend via :term:`GraphQL` (see :ref:`schema`).
       When the backend assigned a :term:`Stream Point` to a listener, the frontend will take care of the connection procedure to the :term:`Stream`, such that the listener can listen to the stream.
   * - :ref:`Backend <caster-back>`
     - Stores information about streams and story graphs and manages their coordination
   * - :ref:`Editor <caster-editor>`
     - Create and edit story graphs within the browser
   * - Sound
     - Wraps the output of :term:`scsynth` into a :term:`WebRTC` stream via :term:`Janus`.
       This is the streaming server of Gencaster.

.. graphviz::
  :caption: The services of Gencaster

    digraph Gencaster {
        node [shape=box, fontname="Arial"]
        edge [fontname="Arial"]

        "Caster sound"
        { rank = source; "Backend" }
        "Frontend"
        "Editor"
        "OSC server"
        { rank = sink; "Listener" [shape="signature", label="Listener" style="filled" color="#adff00"] }
        "Database" [shape="cylinder"]

        "Backend" -> "OSC server" [dir=both, label="OSC"]
        "OSC server" -> "Caster sound" [dir=both, label="OSC"]
        "Backend" -> "Frontend" [dir=both, label="GraphQL"]
        "Listener" -> "Frontend" [label="http"]
        "Caster sound" -> "Frontend" [dir=both, label="WebRTC"]
        "Editor" -> "Backend" [dir=both, label="GraphQL"]
        "Backend" -> "Database" [dir=both]
    }

.. toctree::
   :maxdepth: 3
   :caption: Contents:
   :hidden:

   back/index.rst
   editor.rst
