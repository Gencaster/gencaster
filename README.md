# GenCaster

An web environment for generative audio streams with low latency and device agnostic thanks to WebRTC.

## Services

Service | Comment
--- | ---
CasterBack | Django backend for management of streams
CasterFront | Vue Frontend for user interaction
CasterSound | Janus server for WebRTC streams of SuperCollider audio

## Development

Please use [`pre-commit`](https://pre-commit.com/) before committing to the repository.

The services can be started with `docker-compose up`.

## Deployment

### Network

As the connection of WebRTC relies on delicate network routing we deploy the Janus service in docker network mode `host` instead of `bridge` which puts every service behind a NAT.
The `host` method has the disadvantage that every port we expose within our container is also exposed on our host which an lead to port clashes as well as security problems so please be sure that the firewall is set up correctly.

As WebRTC only works within a SSL environment we use a nginx reverse proxy to forward the port `8089` to the local port `8088` which is the http version of the Janus server.
By doing this we can let nginx handle the SSL context and not need to embed this into Janus.
