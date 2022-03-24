#!/bin/sh

if [ -z "$1" ]; then
    echo "Provide number of sc instances to spawn as argument"
    exit 1
fi


if [[ -z "${SC_ACTIVATE_INPUT}" ]]; then
    echo "Use no inputs"
    USE_INPUT=0
else
    echo "Use inputs"
    USE_INPUT=1
fi

SC_LANG_START_PORT=57120
SC_SYNTH_START_PORT=5600
JANUS_START_PORT_OUT=5002
JANUS_START_PORT_IN=6002

COUNT=0

until [ $COUNT -ge $1 ]; do
    export SC_NAME="SuperCollider$COUNT"
    export SC_PORT=$(($COUNT + $SC_SYNTH_START_PORT))
    export SC_LANG_PORT=$(($COUNT + $SC_LANG_START_PORT))
    export JANUS_OUT_PORT=$(($COUNT + $JANUS_START_PORT_OUT))
    export JANUS_IN_PORT=$(($COUNT + $JANUS_START_PORT_IN))

    echo "### Start instance $SC_NAME on port $SC_LANG_PORT ###"
    sclang -u "$SC_LANG_PORT" /root/sc.scd &> "/root/sclang_$COUNT.log" &
    sleep 3

    echo "Create gstreamer out pipeline on port $JANUS_OUT_PORT"
    gst-launch-1.0 jackaudiosrc port-pattern=$SC_NAME ! queue ! audioconvert ! audioresample ! opusenc ! rtpopuspay ! queue max-size-bytes=0 max-size-buffers=0 ! udpsink host=127.0.0.1 port=$JANUS_OUT_PORT &> "/root/gstreamer_out_$COUNT.log" &

    if [ $USE_INPUT -gt 0 ]; then
        echo "Create gstreamer in pipeline on port $JANUS_IN_PORT"
        gst-launch-1.0 -m udpsrc port="$JANUS_IN_PORT" ! 'application/x-rtp, media=(string)audio, encoding-name=(string)OPUS, payload=(int)100, rate=48000, channels=(int)2' ! rtpopusdepay ! opusdec ! queue ! audioconvert ! audiorate ! audioresample ! jackaudiosink port-pattern="$SC_NAME"
    fi

    COUNT=$(($COUNT + 1))
done

# parallel --tagstring "{}:" --line-buffer tail -f {} ::: janus.log pipewire.log sclang1.log sclang2.log gstreamer-in1.log

echo "Finish"
