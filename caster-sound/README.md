# GenCaster Sound

A SuperCollider instance within a Docker container whose audio is streamed via WebRTC, therefore make it possible to render audio on a server and send it to a client (e.g. a smartphone).

Because WebRTC is used the delay is rather small, below 1 second.

## Usage

If you do not want to use the `docker-compose.yml` file you can build and start the container manually via

```shell
./start_container.sh
```

The container is called `caster-sound`.

To test the functionality of the container you can use a provided webpage which you can spawn via

```shell
python3 -m http.server 9000
```

and go to [http://localhost:9000/test](http://localhost:9000/test).

## Services

The container consitst of

Service | Comment
--- | ---
SuperCollider | Audio engine
Jack | Virtual soundcard on linux
ffmpeg | Swiss army knife for converting media
Janus | Server which distributes media via WebRTC

The services are chained like this

```text
SUPERCOLLIDER --> JACK --> FFMPEG --RTC--> JANUS
```

## Remarks

Except for ffmpeg we use custom builds for every service because

* SuperCollider is build with qt and therefore needs a display
* Janus needs a special version of `libsrtp` which is not provided by `apt-get` (see [here](https://github.com/meetecho/janus-gateway/issues/2024))

Some resources that came in handy

* [ffmpeg and jack](http://underpop.online.fr/f/ffmpeg/help/jack.htm.gz)
