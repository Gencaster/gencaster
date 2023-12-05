.. _caster-back:

Caster Back
===========

*caster-back* is the backend of Gencaster written in Django which takes care of all database, file storage and connection management.

It communicates with the frontend and the editor through GraphQL (see ``caster-back/operations.gql``) which allows to write less back- and frontend communication code in trade for writing more query code.
Through this we also gain the proper types, making use of the TypeScript functionality.

The communication with *caster-sound*, the sound generating and streaming service of Gencaster, is handled through OSC which is an UDP based protocol and is handeled by the *OSC server* service which communicates with *caster-back* through the database.


Global model graph
------------------

.. figure:: ../graphs/global.svg

    Global model graph


.. toctree::
    :hidden:

    osc_server.rst
    story_graph.rst
    stream.rst
    gencaster.rst
