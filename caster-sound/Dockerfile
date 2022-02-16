FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN adduser sc && \
    usermod -a -G audio sc

RUN apt update

RUN apt-get install --yes \
    git \
    g++ \
    python3

RUN mkdir -p /home/sc/tmp
WORKDIR /home/sc/tmp

## jack

# RUN apt-get install --yes \
#     pkg-config \
#     alsa-base \
#     alsa-utils 

RUN git clone https://github.com/jackaudio/jack2.git && \
    cd /home/sc/tmp/jack2 && \
    ./waf configure && \
    ./waf && \
    ./waf install && \
    ldconfig && \
    cd /home/sc/tmp && \
    rm -rf jack2

# supercollider
# from https://github.com/supercollider/supercollider/blob/develop/README_RASPBERRY_PI.md

RUN apt-get install --yes \
    libsamplerate0-dev \
    libsndfile1-dev \
    libasound2-dev \
    libavahi-client-dev \
    libreadline-dev \
    libfftw3-dev \
    libudev-dev \
    libncurses5-dev \
    cmake

RUN git clone --recurse-submodules --branch 3.11 https://github.com/supercollider/supercollider.git && \
    cd supercollider && \
    mkdir build

WORKDIR /home/sc/tmp/supercollider/build

RUN cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DSUPERNOVA=OFF \
    -DSC_ED=OFF \
    -DSC_EL=OFF \
    -DSC_VIM=ON \
    -DNATIVE=ON \
    -DSC_IDE=OFF \
    -DNO_X11=ON \
    -DSC_QT=OFF \
    ..

RUN cmake \
    --build . \
    --config Release \
    --target all

RUN cmake \
    --build . \
    --config Release \
    --target install && \
    ldconfig

# FIX in sc 3.11
RUN rm -rf /usr/local/share/SuperCollider/SCClassLibrary/deprecated/3.13

# RUN usermod -a -G audio root

# USER sc
# USER root

WORKDIR /home/sc

COPY start.sh /home/sc/start.sh
RUN chmod +x /home/sc/start.sh

COPY test.scd .

# CM" ]

# change memory limits of docker
# see https://askubuntu.com/questions/166126/unable-to-start-jack-cannot-allocate-memory
# and
# https://github.com/osetinsky/pulse-streamer/blob/jack-sc/examples/supercollider/99-realtime.conf
#RUN echo "@audio hard    memlock 999999999" >> /etc/security/limits.conf
#RUN echo "@audio hard    rtprio  99" >> /etc/security/limits.conf
# USER sc

# CMD [ "xvfb-run", "sclang" ]