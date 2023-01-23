# GenCaster

An web environment for generative audio streams with low latency and device agnostic thanks to WebRTC.

## Services

To give an overview of the project we will state the function of the different services described in the `docker-compose.yaml` file.
For service specific details check the `README.md` within each folder.

Service | Folder | Port | Comment
--- | --- | --- | ---
`backend` | `caster-back` | `8081` | Django backend with database management for streams
`osc_backend` | `caster-back` | `57130` | OSC server to receive OSC messages from SuperCollider and insert them into the database
`editor` | `caster-editor` | `3001` | Editor fronted for story graphs
`frontend` | `caster-front` | `3000` | Nuxt frontend for user interaction
`sound` | `caster-sound` | `57120`, `8088` | SuperCollider server which can be listened to via WebRTC.
`database` | | `5432` | A postgres database.
`redis` | | | In memory database to distribute messages in our backend

## Documentation

This project is documented via Sphinx.
The documentation sources are in the folder `docs` and the documentation
can be build by executing

```shell
make docs
```

Be sure to run this in the proper Python environment (e.g. virtualenv).

## Development

Please install [`pre-commit`](https://pre-commit.com/) and set it up via `pre-commit install` before committing to the repository.

After a commit on the `main` branch it will trigger a re-deployment on the development server.

### Local development

To start a local instance of GenCaster with all its services simply type use `make`

```shell
make docker-local
```

You can use the following flags to modify the stack


flag | comment
--- | ---
`-e` | Starts without the editor
`-s` | Starts without the frontend

**Example:** `make -es docker-local` starts without editor and frontend.

This allows you to use your local host machine in place to develop with auto reload as Docker and NodeJS is not a nice tandem because of the dependence of the `node_modules` folder.

### Server setup

The deployment server requires the following dependencies installed

* `git`
* `make`
* `docker` (with `docker compose`)

Also `nginx` as a reverse proxy is recommended.

### Network

As the connection of WebRTC relies on delicate network routing we deploy the Janus service in docker network mode `host` instead of `bridge` which puts every service behind a NAT.
The `host` method has the disadvantage that every port we expose within our container is also exposed on our host which an lead to port clashes as well as security problems so please be sure that the firewall is set up correctly.

As WebRTC only works within a SSL environment we use a nginx reverse proxy to forward the port `8089` to the local port `8088` which is the http version of the Janus server.
By doing this we can let nginx handle the SSL context and not need to embed this into Janus.
