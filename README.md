# [Gencaster](https://gencaster.org)

<p align="center">
  <img width="200" height="200" src="./docs/_static/logo.svg">
</p>

**Gencaster** is a non-linear audio streaming framework for real-time radiophonic experiences and live music and consists of multiple services.

The audio streams have a low latency (about 150ms) and can be listened to in any modern browser, and can dynamically render audio content based on a given *story graph* that can react to user input such as name, time, GPS position, or even microphone streaming after permissions have been granted.

* *caster-sound* is a service that handles all streaming and audio rendering functionality, using [SuperCollider](https://supercollider.github.io/) to generate audio and [Janus](https://janus.conf.meetecho.com) to distribute audio to listeners via [WebRTC](https://janus.conf.meetecho.com)

* *caster-back* is a web backend to manage the streams of *caster-sound*, written in [Django](https://www.djangoproject.com/)

* *caster-front* is a web frontend that allows users to listen to the streams of *caster-sound*, written in [Vue](https://vuejs.org/)

* *caster-editor* is a web-editor in which the actions of a stream, called a *story graph*, can be created, edited and tweaked using Python or SuperCollider, and is also written in [Vue](https://vuejs.org/)


For further information please visit

* [Project website gencaster.org](https://gencaster.org)
* [Documentation](https://gencaster.github.io/gencaster)

## Documentation

Gencaster uses [Sphinx](https://www.sphinx-doc.org/en/master/) for documentation and can be accessed online via GitHub pages at [gencaster.github.io/gencaster](https://gencaster.github.io/gencaster).
The sources for the documentation are located in the `./docs` directory and can be build locally by executing

```shell
make docs
```

## Development

In order to have consistent styles and a good history Gencaster uses [`pre-commit`](https://pre-commit.com/).
After installation of pre-commit and cloning the repository the necessary scripts can be set up via `pre-commit install`.

### Local development

To start a local instance of Gencaster with all its services using [Docker](https://www.docker.com/) simply use

```shell
make docker-local
```

There are additional flags to control which services are spawned

flag | comment
--- | ---
`no-editor=1` | Starts without the editor
`no-frontend=1` | Starts without the frontend
`no-sound=1` | Starts without the frontend

**Example:** `make no-editor=1 no-frontend=1 docker-local` starts without editor and frontend.

This allows e.g. to have access to the Gencaster backend but use the host environment to develop the editor and frontend as development with NodeJS within Docker is a bit complicated due to the shared `node_modules` directory.

### Network

As the connection of WebRTC relies on delicate network routing we deploy the Janus service in docker network mode `host` instead of `bridge` which puts every service behind a NAT.
The `host` method has the disadvantage that every port we expose within our container is also exposed on our host which an lead to port clashes as well as security problems so please be sure that the firewall is set up correctly.

As WebRTC only works within a SSL environment we use a nginx reverse proxy to forward the port `8089` to the local port `8088` which is the http version of the Janus server.
By doing this we can let nginx handle the SSL context and not need to embed this into Janus.

## Copyright

© 2023 Vinzenz Aubry and Dennis Scheiba

## License

APGL-3.0
