# GenCaster Sound

A SuperCollider instance within a Docker container whose audio is streamed via WebRTC, therefore make it possible to render audio on a server and send it to a client (e.g. a smartphone).

Because WebRTC is used the delay is rather small, below 1 second.

## Usage

If you do not want to use the `docker-compose.yml` file you can build and start the container manually via

```shell
./start_container.sh
```

The container is called `caster-sound`.

One can listen to the stream on and go to [http://127.0.0.1:8090](http://127.0.0.1:8090).

## Services

The container consitst of

Service | Comment
--- | ---
Supervisor | As we need multiple services in this container we use this for service management - something like systemd
SuperCollider | Audio engine
pipewire | Acts as a virtual soundcard. Used to be jack but pipewire seems more reliable within a container environment.
gstreamer | Swiss army knife for converting media - converts the output of SuperCollider to a opus RTP stream which is send to *Janus*
Janus | Server which distributes media via WebRTC
Python HTTP Server | Server on port `8090` in which one can listen to the generated stream - this is only for debug purposes.

The services are chained like this

```text
SUPERCOLLIDER --> PIPEWIRE --> GSTREAMER --RTC--> JANUS
```

## Remarks

Used to be a `ubuntu:21.04` container but this needed much
custom compilation.
With *Alpine* we can use newer binaries which fix bugs of old versions
so we only need to compile *SuperCollider* and *janus*.
Check the `Dockerfile` for remarks.
