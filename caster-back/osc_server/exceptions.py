class MalformedOscMessage(Exception):
    """OSC message has wrong layout."""


class OscBackendAuthException(Exception):
    """Authentication failed."""
