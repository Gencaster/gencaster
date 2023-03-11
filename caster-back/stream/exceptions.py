"""
Exceptions
==========
"""


class NoStreamAvailableException(Exception):
    """No stream available"""


class InvalidAudioFileException(Exception):
    """Invalid audio file.
    This is necessary as the API accepts empty files so we can not
    use the data model validation but need to implement a validation
    by ourselves.
    """
