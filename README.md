# GenCaster

An web environment for generative audio streams with low latency and device agnostic thanks to WebRTC.

## Services

To give an overview of the project we will state the function of the different services described in the `docker-compose.yaml` file.
For service specific details check the `README.md` within each folder.

Service | Folder | Port | Comment
--- | --- | --- | ---
`backend` | `caster-back` | `8081` | Django backend with database management for streams
`osc_backend` | `caster-back` | `57130` | OSC server to receive OSC messages from SuperCollider and insert them into the database
`frontend` | `caster-front` | `3000` | Nuxt frontend for user interaction
`sound` | `caster-sound` | `57120`, `8088` | SuperCollider server which can be listened to via WebRTC.
`database` | | `5432` | A postgres database.

## Development

Please use [`pre-commit`](https://pre-commit.com/) before committing to the repository.

The services can be started with `docker-compose up`.

## Deployment

### Network

As the connection of WebRTC relies on delicate network routing we deploy the Janus service in docker network mode `host` instead of `bridge` which puts every service behind a NAT.
The `host` method has the disadvantage that every port we expose within our container is also exposed on our host which an lead to port clashes as well as security problems so please be sure that the firewall is set up correctly.

As WebRTC only works within a SSL environment we use a nginx reverse proxy to forward the port `8089` to the local port `8088` which is the http version of the Janus server.
By doing this we can let nginx handle the SSL context and not need to embed this into Janus.
