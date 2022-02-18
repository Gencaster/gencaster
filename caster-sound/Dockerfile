FROM ubuntu:21.04

ENV DEBIAN_FRONTEND noninteractive

RUN adduser sc

RUN mkdir -p /home/sc/tmp

WORKDIR /home/sc/tmp

RUN apt-get update && \
	apt-get install -y \
		git \
		wget \
		build-essential

# --- JANUS ----------------------------------

RUN apt-get install -y \
	libmicrohttpd-dev \
	libjansson-dev \
	libssl-dev \
	libsrtp2-dev \
	libsofia-sip-ua-dev \
	libglib2.0-dev \
	libopus-dev \
	libogg-dev \
	libcurl4-openssl-dev \
	liblua5.3-dev \
	libconfig-dev \
	pkg-config \
	gengetopt \
	libtool \
	automake

# libsrtp
WORKDIR /home/sc/tmp
RUN apt remove -y libsrtp2-1 libsrtp2-dev
RUN wget https://github.com/cisco/libsrtp/archive/v2.2.0.tar.gz && \
	tar xfv v2.2.0.tar.gz
WORKDIR /home/sc/tmp/libsrtp-2.2.0
RUN ./configure --prefix=/usr --enable-openssl && \
	make shared_library && \
	make install && \
    rm -rf /home/sc/tmp/*

# libnice
WORKDIR /home/sc/tmp
RUN wget https://libnice.freedesktop.org/releases/libnice-0.1.18.tar.gz && \
	tar xzf libnice-0.1.18.tar.gz
WORKDIR /home/sc/tmp/libnice-0.1.18
RUN apt-get remove libnice-dev && \
	apt-get install -y meson ninja-build
RUN meson --prefix=/usr build && \
	/usr/bin/ninja -C build && \
	/usr/bin/ninja -C build install && \
    rm -rf /home/sc/tmp/* 

WORKDIR /home/sc/tmp
RUN git clone --depth 1 --branch v0.11.6 \
	https://github.com/meetecho/janus-gateway.git
WORKDIR /home/sc/tmp/janus-gateway
RUN ./autogen.sh && \
	./configure --prefix=/opt/janus \
		--disable-rabbitmq \
		--disable-mqtt && \
	make -j4 && \
	make install && \
	make configs && \
    rm -rf /home/sc/tmp/*

# --- FFMPEG ---------------------------------

RUN apt-get install --yes ffmpeg

# --- JACK -----------------------------------

WORKDIR /home/sc/tmp
RUN git clone --depth 1 --branch v1.9.19 \
	git://github.com/jackaudio/jack2.git
WORKDIR /home/sc/tmp/jack2
RUN ./waf configure && \
	./waf && \
	./waf install && \
	ldconfig && \
    rm -rf /home/sc/tmp/*

# --- SUPERCOLLIDER --------------------------

# https://github.com/supercollider/supercollider/blob/develop/README_RASPBERRY_PI.md
# For GUI-less builds:
RUN apt-get install -y \
	libsamplerate0-dev \
	libsndfile1-dev \
	libasound2-dev \
	libavahi-client-dev \
    libreadline-dev \
	libfftw3-dev \
	libudev-dev \
	libncurses5-dev \
	cmake
WORKDIR /home/sc/tmp
RUN git clone --depth 1 --branch 3.11 --recurse-submodules https://github.com/supercollider/supercollider.git
WORKDIR /home/sc/tmp/supercollider
RUN mkdir build && cd build && \
	cmake \
		-DCMAKE_BUILD_TYPE=Release \
		-DSUPERNOVA=OFF \
		-DSC_ED=OFF \
		-DSC_EL=OFF \
		-DSC_VIM=ON \
		-DNATIVE=ON \
		-DSC_IDE=OFF \
		-DNO_X11=ON \
		-DSC_QT=OFF .. && \
	cmake --build . --config Release --target all && \
	cmake --build . --config Release --target install && \
	ldconfig && \
    rm -rf /home/sc/tmp/*

# --------------------------------------------


WORKDIR /home/sc

COPY start_services.sh .
# RUN chmod +x /home/sc/start_services.sh

COPY sc.scd .

CMD ["/bin/sh", "./start_services.sh"]
