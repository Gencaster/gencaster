#!/bin/sh

docker build -t caster_sound .


docker run \
	--rm \
	--name sc-sound \
	--publish=10000-10200:10000-10200 \
	--publish=8188:8188 \
	--publish=8088:8088 \
	--publish=8089:8089 \
	--publish=8889:8889 \
	--publish=8000:8000 \
	--publish=7088:7088 \
	--publish=7089:7089 \
	--publish=8090:8090 \
    --publish=8050:80 \
	--net bridge \
	caster_sound
