from django.shortcuts import render
from asgiref.sync import sync_to_async

from gencaster.asgi import sio, osc_client
from voice.models import TextToSpeech


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


@sio.event
async def disconnect(sid):
    print("Client disconnected")
