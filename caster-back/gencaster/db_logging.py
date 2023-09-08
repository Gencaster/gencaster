import enum
import logging
from logging import LogRecord
from typing import TYPE_CHECKING, Generic, Optional, TypeVar

if TYPE_CHECKING:
    from stream.models import Stream, StreamPoint
T = TypeVar("T", "Stream", "StreamPoint")

TO_DB_FLAG = "to_db"


class LogKeyEnum(str, enum.Enum):
    STREAM_POINT = "stream_point"
    STREAM = "stream"


class LogContext:
    """It is necessary to attach the filter to the log handlers
    and not to the logger instance because otherwise the filter
    will not propagate.
    """

    # see https://stackoverflow.com/questions/6850798/why-doesnt-filter-attached-to-the-root-logger-propagate-to-descendant-loggers
    def __init__(
        self, key: LogKeyEnum, value: T, logger: Optional[logging.Logger] = None
    ) -> None:
        self.logger: logging.Logger = logger if logger else logging.getLogger()
        self.filter: GencasterLogFilter = GencasterLogFilter(key, value)

    def __enter__(self):
        for handler in self.logger.handlers:
            # if type(handler) == 'DatabaseLoggingHandler':
            handler.addFilter(self.filter)

    def __exit__(self, *args, **kwargs):
        for handler in self.logger.handlers:
            # if type(handler) == 'DatabaseLoggingHandler':
            handler.removeFilter(self.filter)


class GencasterLogFilter(Generic[T], logging.Filter):
    # inspired by https://docs.python.org/3/howto/logging-cookbook.html#using-filters-to-impart-contextual-information
    # combined with a generics approach
    def __init__(self, key: LogKeyEnum, value: T) -> None:
        self.key = key
        self.value: T = value
        logging.Filter.__init__(self, name="")

    def filter(self, record: LogRecord) -> bool:
        if any(
            [record.name.startswith(x) for x in ["gencaster", "stream", "story_graph"]]
        ):
            setattr(record, self.key, self.value)
            setattr(record, TO_DB_FLAG, True)
        return logging.Filter.filter(self, record)
