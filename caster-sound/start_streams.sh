#!/bin/sh

if [ -z "$1" ]; then
    if [[ -z "${SUPERCOLLIDER_NUM_STREAMS}" ]]; then
        echo "Provide number of sc instances to spawn as argument or as env variable SUPERCOLLIDER_NUM_STREAMS"
        exit 1
    else
        NUM_STREAMS=$SUPERCOLLIDER_NUM_STREAMS
    fi
    NUM_STREAMS=$SUPERCOLLIDER_NUM_STREAMS
fi


if [[ -z "${SUPERCOLLIDER_USE_INPUT}" ]]; then
    echo "Create no input streams"
    USE_INPUT=0
else
    echo "Create input streams"
    USE_INPUT=1
fi

SC_LANG_START_PORT=57120
SC_SYNTH_START_PORT=5600
JANUS_START_PORT_OUT=5002
JANUS_START_PORT_IN=6002

echo "Spawn $NUM_STREAMS instances"

COUNT=1

until [ $COUNT -gt $NUM_STREAMS ]; do
    export SC_NAME="SuperCollider$COUNT"
    # -1 b/c we start iterating at 1
    export SC_PORT=$(($COUNT + $SC_SYNTH_START_PORT - 1))
    export SC_LANG_PORT=$(($COUNT + $SC_LANG_START_PORT - 1))
    export JANUS_OUT_PORT=$(($COUNT + $JANUS_START_PORT_OUT - 1))
    export JANUS_OUT_ROOM=$(($COUNT))
    export JANUS_IN_PORT=$(($COUNT + $JANUS_START_PORT_IN - 1))
    export JANUS_IN_ROOM=$(($COUNT))

    echo "### Start instance $SC_NAME on port $SC_LANG_PORT ###"

    (sclang -u "$SC_LANG_PORT" /root/sc.scd &> "/root/sclang_$COUNT.log") &

    sleep 10
    echo "Create gstreamer out pipeline on port $JANUS_OUT_PORT"
    (gst-launch-1.0 jackaudiosrc port-pattern=$SC_NAME ! queue ! audioconvert ! audioresample ! opusenc ! rtpopuspay ! queue max-size-bytes=0 max-size-buffers=0 ! udpsink host=127.0.0.1 port=$JANUS_OUT_PORT &> "/root/gstreamer_out_$COUNT.log") &

    if [ $USE_INPUT -gt 0 ]; then
        echo "Create gstreamer in pipeline on port $JANUS_IN_PORT"
        (gst-launch-1.0 -m udpsrc port="$JANUS_IN_PORT" ! 'application/x-rtp, media=(string)audio, encoding-name=(string)OPUS, payload=(int)100, rate=48000, channels=(int)2' ! rtpopusdepay ! opusdec ! queue ! audioconvert ! audiorate ! audioresample ! jackaudiosink port-pattern="$SC_NAME" &> "/root/gstreamer_in_$COUNT.log") &
    fi

    COUNT=$(($COUNT + 1))
done

parallel --tagstring "{}:" --line-buffer tail -f {} ::: sclang_*.log

echo "Finish"
