.. _deployment:

Deployment
==========

Docker
------

As the setup of the streaming stack is delicate the only supported way of deployment is via `docker compose` which automates most of the setup procedure.
Yet it is still necessary to provide some config files which are described here.

``.secrets.env``
^^^^^^^^^^^^^^^^

Sensitive information such as passwords are stored in ``.secrets.env`` which is not part of the repository and needs therefore be created in order to spin up the containers.

A local setup can look like this

.. code-block:: text

  GOOGLE_APPLICATION_CREDENTIALS="/path/to/gcp.json"


while a dev deployment can look like this

.. code-block:: text

  GOOGLE_APPLICATION_CREDENTIALS="/path/to/gcp.json"

  DJANGO_SU_USER=changeMe
  DJANGO_SU_PASS=changeMe

  POSTGRES_DB=gencaster
  POSTGRES_PASSWORD=changeMe
  POSTGRES_USER=gencaster

  BACKEND_OSC_PASSWORD=changeMe

  SENTRY_DSN_CASTER_BACK="https://changeMe.io"
  SENTRY_DSN_CASTER_EDITOR="https://changeMe.io"
  SENTRY_DSN_CASTER_FRONT="https://changeMe.io"


.. _deployment-services:

Services
^^^^^^^^

.. list-table:: Docker services
   :widths: 25 25 25 25
   :header-rows: 1

   * - Service
     - Port
     - Comment
     - Documentation
   * - ``backend``
     - ``8081``
     - Django backend with database management for streams
     - :ref:`caster-back`
   * - ``osc_backend``
     - ``57130``
     - OSC server to receive OSC messages from SuperCollider and insert them into the database
     - :ref:`OSC Server`
   * - ``editor``
     - ``3001``
     - Editor fronted for story graphs
     - :ref:`caster-editor`
   * - ``frontend``
     - ``3000``
     - frontend for user interaction
     - :ref:`caster-front`
   * - ``sound``
     - ``57120,8088``
     - SuperCollider server which can be listened to via WebRTC
     - :ref:`caster-sound`
   * - ``database``
     - ``5432``
     - Postgres database for the backend
     -
   * - ``redis``
     -
     - In memory database for pub/sub management of backend
     -

UFW
---

It is necessary to adjust the firewall to forward any WebRTC traffic.
A config for `UFW <https://wiki.archlinux.org/title/Uncomplicated_Firewall>`_ can look like this.

.. code-block::

    ufw status
    Status: active

    To                         Action      From
    --                         ------      ----
    22                         ALLOW       Anywhere
    80                         ALLOW       Anywhere
    443                        ALLOW       Anywhere
    8089                       ALLOW       Anywhere
    10000:10200/udp            ALLOW       Anywhere
    50000:60000/udp            ALLOW       Anywhere
    10000:60000/udp            ALLOW       Anywhere
    57120                      ALLOW       Anywhere
    8090                       ALLOW       Anywhere
    22 (v6)                    ALLOW       Anywhere (v6)
    80 (v6)                    ALLOW       Anywhere (v6)
    443 (v6)                   ALLOW       Anywhere (v6)
    8089 (v6)                  ALLOW       Anywhere (v6)
    10000:10200/udp (v6)       ALLOW       Anywhere (v6)
    50000:60000/udp (v6)       ALLOW       Anywhere (v6)
    10000:60000/udp (v6)       ALLOW       Anywhere (v6)
    57120 (v6)                 ALLOW       Anywhere (v6)
    8090 (v6)                  ALLOW       Anywhere (v6)

    10000:10200/udp            ALLOW OUT   Anywhere
    8089                       ALLOW OUT   Anywhere
    10000:10200/udp (v6)       ALLOW OUT   Anywhere (v6)
    8089 (v6)                  ALLOW OUT   Anywhere (v6)

Ngingx
------

An nginx config could look like this

.. code-block::

    # frontend
    server {
        server_name dev.gencaster.org;

        charset utf-8;

        location = /favicon.ico { access_log off; log_not_found off; }
        location = /robots.txt  { access_log off; log_not_found off; }

        access_log /var/log/nginx/dev.gencaster.org-access.log;
        error_log  /var/log/nginx/dev.gencaster.org-error.log error;

        location / {
            # add_header Access-Control-Allow-Origin *;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_http_version 1.1;

            proxy_pass http://127.0.0.1:3000/;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }

        listen [::]:443 ssl; # managed by Certbot
        listen 443 ssl; # managed by Certbot
        ssl_certificate /etc/letsencrypt/live/dev.gencaster.org/fullchain.pem; # managed by Certbot
        ssl_certificate_key /etc/letsencrypt/live/dev.gencaster.org/privkey.pem; # managed by Certbot
        include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

    }

    # backend
    server {
        server_name backend.dev.gencaster.org;

        client_max_body_size 4G;
        charset utf-8;

        location = /favicon.ico { access_log off; log_not_found off; }
        location = /robots.txt  { access_log off; log_not_found off; }

        access_log /var/log/nginx/dev.gencaster.org-access.log;
        error_log  /var/log/nginx/dev.gencaster.org-error.log error;

        location / {
            # add_header Access-Control-Allow-Origin *;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # new
        proxy_redirect off;

            proxy_http_version 1.1;

            proxy_pass http://127.0.0.1:8081;
        }

        listen [::]:443 ssl; # managed by Certbot
        listen 443 ssl; # managed by Certbot
        ssl_certificate /etc/letsencrypt/live/dev.gencaster.org/fullchain.pem; # managed by Certbot
        ssl_certificate_key /etc/letsencrypt/live/dev.gencaster.org/privkey.pem; # managed by Certbot
        include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

    }

    # editor
    server {
        server_name editor.dev.gencaster.org;

        charset utf-8;

        location = /favicon.ico { access_log off; log_not_found off; }
        location = /robots.txt  { access_log off; log_not_found off; }

        access_log /var/log/nginx/dev.gencaster.org-access.log;
        error_log  /var/log/nginx/dev.gencaster.org-error.log error;

        location / {
            # add_header Access-Control-Allow-Origin *;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_http_version 1.1;

            proxy_pass http://127.0.0.1:3001/;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }

        listen [::]:443 ssl; # managed by Certbot
        listen 443 ssl; # managed by Certbot
        ssl_certificate /etc/letsencrypt/live/dev.gencaster.org/fullchain.pem; # managed by Certbot
        ssl_certificate_key /etc/letsencrypt/live/dev.gencaster.org/privkey.pem; # managed by Certbot
        include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
    }

    # sound
    server {
        server_name sound.dev.gencaster.org;

        charset utf-8;

        location = /favicon.ico { access_log off; log_not_found off; }
        location = /robots.txt  { access_log off; log_not_found off; }

        access_log /var/log/nginx/dev.gencaster.org-access.log;
        error_log  /var/log/nginx/dev.gencaster.org-error.log error;

        client_max_body_size 255M;

        location / {
            # add_header Access-Control-Allow-Origin *;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_http_version 1.1;

            proxy_pass http://127.0.0.1:8088/;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }

        listen [::]:443 ssl; # managed by Certbot
        listen 443 ssl; # managed by Certbot
        ssl_certificate /etc/letsencrypt/live/dev.gencaster.org/fullchain.pem; # managed by Certbot
        ssl_certificate_key /etc/letsencrypt/live/dev.gencaster.org/privkey.pem; # managed by Certbot
        include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

    }

    # http -> https redirect
    server {
        if ($host = dev.gencaster.org) {
            return 301 https://$host$request_uri;
        } # managed by Certbot


        listen 80;
        listen [::]:80;
        server_name dev.gencaster.org;
        return 404; # managed by Certbot
    }
