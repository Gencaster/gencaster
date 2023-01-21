"""
The OSC server handles the backend communication from SuperCollider.
As OSC useses UDP and it is designed in an async manner we have to send back any result
from SuperCollider via a new OSC message.
As Django does not natively understand UDP messages and OSC is a rather restrictive
protocol we created this server which is able to receive this messages and makes it available
to our Django app by using its ORM.

Each SuperCollider instance sends a beacon in order to get discovered by the backend as a
:class:`~stream.models.StreamPoint`.

This is **not** a Django app but an application on its own.


.. todo::

    A long term goal would be to include this into the Django process but it seems gunicorn
    only runs when a request hits, making the necessary polling for received messages not working
    properly.

.. contents:: :local:
    :depth: 2

.. automodule:: osc_server.server
    :members:

.. automodule:: osc_server.models


.. automodule:: osc_server.exceptions
    :members:

"""
