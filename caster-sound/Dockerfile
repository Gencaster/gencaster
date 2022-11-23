FROM alpine:3.15

ARG MAKE_JOBS=8

WORKDIR /root

# needed for pipewire
ENV XDG_RUNTIME_DIR='/root'

# although we will use pipewire instead of jack we need the
# header bindings which are not available for pipewire-jack
# so we will instead compile against native jack but replace it
# later

RUN apk add \
    jack \
    jack-dev \
    git \
    vim

# ------------------  SUPERCOLLIDER

RUN apk add \
    alsa-lib-dev \
    boost-dev  \
    boost-static  \
    cmake  \
    eudev-dev  \
    fftw-dev  \
    libsndfile-dev  \
    libxt-dev  \
    linux-headers  \
    ncurses-dev  \
    portaudio-dev  \
    readline-dev  \
    samurai  \
    yaml-cpp-dev \
    g++ \
    make

# apply submodule fix
# see https://github.com/supercollider/supercollider/issues/5695#issuecomment-1072263846
RUN git clone \
    --depth 1 \
    --branch 3.12 \
    https://github.com/SuperCollider/SuperCollider.git && \
    cd SuperCollider && \
    sed -i "s|git://|https://|g" .gitmodules && \
    git submodule update --init --recursive && \
    mkdir -p /root/SuperCollider/build

WORKDIR /root/SuperCollider

# apply patch for alpine, see
# https://github.com/supercollider/supercollider/issues/5197#issuecomment-1047188442
COPY sc-alpine.patch .
RUN apk add patch && patch < sc-alpine.patch

WORKDIR /root/SuperCollider/build
RUN cmake \
	-DCMAKE_BUILD_TYPE=Debug \
	-DSUPERNOVA=OFF \
	-DSC_ED=OFF \
	-DSC_EL=OFF \
	-DSC_VIM=ON \
	-DNATIVE=ON \
	-DSC_IDE=OFF \
	-DNO_X11=ON \
	-DSC_ABLETON_LINK=OFF \
	-DSC_QT=OFF .. && \
	cmake --build . --config Debug --target all -j${MAKE_JOBS} && \
    cmake --build . --config Debug --target install -j${MAKE_JOBS} && \
    rm -rf /root/SuperCollider

# now we replace jack with pipewire which is more stable
# in a virtualized environment than jack which resulted
# in an unstable clock and dropouts

RUN apk del \
    jack \
    jack-dev

# ------------------  PIPEWIRE

RUN apk add \
    pipewire \
    pipewire-media-session \
    pipewire-jack \
    pipewire-tools

# ------------------  GSTREAMER

RUN apk add \
    gstreamer \
    gstreamer-dev \
    gst-plugins-good \
    gst-plugin-pipewire \
    gstreamer-tools

# ------------------  SUPERVISOR

RUN apk add supervisor

# ------------------  JANUS

RUN apk add \
    autoconf \
    automake \
    libtool \
    gengetopt \
    lua5.3-dev \
    cmake \
    libsrtp-dev \
	libnice-dev \
    jansson-dev \
    libconfig-dev \
    libusrsctp-dev \
    libmicrohttpd-dev \
	libwebsockets-dev \
    rabbitmq-c-dev \
    curl-dev \
    libogg-dev \
    libopusenc-dev \
	lua \
    duktape-dev \
    npm \
    ffmpeg-dev \
    zlib-dev \
    libogg-dev \
	libuv-dev \
    sofia-sip-dev

WORKDIR /root

RUN git clone --depth 1 --branch "v0.11.8" https://github.com/meetecho/janus-gateway.git && \
    cd janus-gateway && \
    ./autogen.sh && \
    ./configure \
    --prefix=/opt/janus \
    --disable-rabbitmq \
	--disable-mqtt && \
    make -j ${MAKE_JOBS} && \
    make install && \
    make configs && \
    rm -rf /root/janus-gateway

RUN apk add parallel

# ------------------  STATIC HTML FILES
# are served via a python http server - only for debugging
COPY html_test /root/html_test/

# apply config files

COPY janus.plugin.streaming.jcfg /opt/janus/etc/janus/janus.plugin.streaming.jcfg
COPY janus.plugin.audiobridge.jcfg /opt/janus/etc/janus/janus.plugin.audiobridge.jcfg

COPY start_streams.sh /root/start_streams.sh

COPY caster-sound.conf /root/caster-sound.conf

COPY sc.scd /root/sc.scd

COPY GenCaster/ /usr/local/share/SuperCollider/Extensions/GenCaster/

COPY create_config.sh /root/create_config.sh
COPY janus.plugin.audiobridge.jcfg.template /root/janus.plugin.audiobridge.jcfg.template
COPY janus.plugin.streaming.jcfg.template /root/janus.plugin.streaming.jcfg.template

# CMD ["tail", "-f", "/dev/null"]
CMD ["/bin/sh", "-c", "/root/create_config.sh && /usr/bin/supervisord -c /root/caster-sound.conf"]
