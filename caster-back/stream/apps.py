import asyncio
import logging
from logging import Handler, LogRecord
from logging.handlers import QueueHandler, QueueListener
from queue import Queue
from threading import Thread

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.apps import AppConfig


def setup_logging():
    from gencaster.db_logging import TO_DB_FLAG, LogKeyEnum
    from gencaster.distributor import GenCasterChannel, StreamLogUpdateMessage

    class DatabaseLoggingHandler(Handler):
        """
        As we need access to the :class:`stream.models.StreamLog` model it is necessary to delay the
        initialization of the logging mechanism by declaring it within the ``ready`` callback
        of the app setup.

        The setup code below is inspired
        `from the official documentation <https://docs.python.org/3/howto/logging-cookbook.html#dealing-with-handlers-that-block>`_
        but due to the async runtime, the handler spins up its own thread and is inspired from
        https://github.com/CopterExpress/python-async-logging-handler/blob/master/async_logging_handler/__init__.py

        """

        def __init__(self, level: int = logging.DEBUG) -> None:
            self._queue: Queue[logging.LogRecord] = Queue(-1)
            self._thread = Thread(target=self._loop)
            self._thread.daemon = True
            self._thread.start()
            self._channel = get_channel_layer()
            self._event_loop = asyncio.get_event_loop()
            super().__init__(level)

        def _loop(self):
            from .models import StreamLog

            # print("### START LOGGING THREAD LOOP ###")
            while True:
                record = self._queue.get()
                if getattr(record, TO_DB_FLAG, False):
                    stream = getattr(record, LogKeyEnum.STREAM, None)
                    stream_point = getattr(record, LogKeyEnum.STREAM_POINT, None)

                    # stream implies a stream so let's use it if it is not
                    # explicitly set
                    if stream is not None and stream_point is None:
                        stream_point = stream.stream_point

                    stream_log = StreamLog.objects.create(
                        stream=stream,
                        stream_point=stream_point,
                        origin=getattr(record, "origin", None),
                        message=record.getMessage(),
                        level=record.levelno,
                        name=record.name,
                    )

                    async_to_sync(GenCasterChannel.send_log_update)(
                        self._channel,
                        StreamLogUpdateMessage(
                            uuid=str(stream_log.uuid),
                            stream_point_uuid=str(stream_point.uuid)
                            if stream_point
                            else None,
                            stream_uuid=str(stream.uuid) if stream else None,
                        ),
                    )

        def emit(self, record: LogRecord) -> None:
            self._queue.put(record)

    # see https://docs.python.org/3/howto/logging-cookbook.html#dealing-with-handlers-that-block
    log_queue: Queue = Queue(-1)

    root_logger = logging.getLogger()
    QueueHandler(log_queue)

    db_handler = DatabaseLoggingHandler()
    db_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(db_handler)
    root_logger.setLevel(logging.DEBUG)
    queue_listener = QueueListener(log_queue, db_handler)
    queue_listener.start()


class StreamConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stream"

    def disconnect_running_streams(self):
        from .models import Stream

        try:
            Stream.objects.disconnect_all_streams()
        except Exception:
            pass

    def ready(self) -> None:
        self.disconnect_running_streams()
        setup_logging()
        return super().ready()
