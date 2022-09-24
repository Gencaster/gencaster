import logging
from typing import Dict

from asgiref.sync import sync_to_async
from django.shortcuts import render

from gencaster.asgi import osc_client, sio
from stream.exceptions import NoStreamAvailable
from stream.models import OSCMessage, Stream
from voice.models import TextToSpeech

log = logging.getLogger(__name__)


def speak_on_stream(text: str) -> TextToSpeech:
    text_to_speech = TextToSpeech(text=f"<speak>{text}</speak>")
    text_to_speech.generate_sound_file()
    osc_client.send_message("/speak", text_to_speech.audio_file.name)
    return text_to_speech


def index(request):
    return render(request, "stories/index.html")


@sio.event
async def my_event(sid, message):
    await sio.emit("my_response", {"data": message["data"]}, room=sid)


@sio.event
async def my_broadcast_event(sid, message):
    log.info(f"We received a broadcast message: {message}")
    await sync_to_async(speak_on_stream, thread_sensitive=True)(text=message["data"])
    await sio.emit("my_response", {"data": message["data"]})


@sio.event
async def join(sid, message):
    sio.enter_room(sid, message["room"])
    await sio.emit(
        "my_response", {"data": "Entered room: " + message["room"]}, room=sid
    )


@sio.event
async def leave(sid, message):
    sio.leave_room(sid, message["room"])
    await sio.emit("my_response", {"data": "Left room: " + message["room"]}, room=sid)


@sio.event
async def close_room(sid, message):
    await sio.emit(
        "my_response",
        {"data": "Room " + message["room"] + " is closing."},
        room=message["room"],
    )
    await sio.close_room(message["room"])


@sio.event
async def my_room_event(sid, message):
    await sio.emit("my_response", {"data": message["data"]}, room=message["room"])


@sio.event
async def disconnect_request(sid):
    await sio.disconnect(sid)


@sio.event
async def connect(sid, environ):
    await sio.emit("my_response", {"data": "Connected", "count": 0}, room=sid)


@sio.on("getStream")
async def get_stream(sid):
    sio_session = await sio.get_session(sid)
    if "streamUUID" in sio_session:
        log.info(
            f"Stream request rejected b/c already attached a stream ({sio_session['streamUUID']})"
        )
        return
    try:
        stream: Stream = await sync_to_async(Stream.objects.get_free_stream)()
    except NoStreamAvailable:
        log.info("No free stream available")
        # todo give feedback to frontend
        return
    await sio.save_session(sid, {"streamUUID": str(stream.uuid)})
    await sio.emit(
        "setStream",
        {
            "streamUUID": str(stream.uuid),
            "streamPoint": {
                "janus_out_room": stream.stream_point.janus_out_room,
            },
        },
    )


@sio.on("gps")
async def receive_gps(sid, data: Dict) -> None:
    sio_session = await sio.get_session(sid)
    if "streamUUID" not in sio_session:
        log.error("Can not find stream for GPS data")
        return
    stream: Stream = await sync_to_async(
        Stream.objects.select_related("stream_point").get
    )(uuid=sio_session["streamUUID"])
    assert stream.active
    log.debug(f"Received GPS location ({data}) for stream {sio_session['streamUUID']}")
    stream.stream_point.send_osc_message(
        OSCMessage.from_dict(
            "/gps",
            data=data,
        )
    )
    return


@sio.event
async def disconnect(sid):
    sio_session = await sio.get_session(sid)
    try:
        stream = await sync_to_async(Stream.objects.get)(uuid=sio_session["streamUUID"])
        await sync_to_async(stream.disconnect)()
    except KeyError:
        log.info(f"Leaving user had no stream attached")
    print("Client disconnected")
