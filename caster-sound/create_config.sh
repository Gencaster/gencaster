#!/bin/sh

# from start_stream.sh
SC_LANG_START_PORT=57120
SC_SYNTH_START_PORT=5600
JANUS_START_PORT_OUT=5002
JANUS_START_PORT_IN=6002

# reset configs
echo "" > "/opt/janus/etc/janus/janus.plugin.audiobridge.jcfg"
echo "" > "/opt/janus/etc/janus/janus.plugin.streaming.jcfg"

COUNT=1;
until [ $COUNT -gt $SUPERCOLLIDER_NUM_STREAMS ]; do
    export JANUS_OUT_PORT=$(($COUNT + $JANUS_START_PORT_OUT - 1))
    export JANUS_OUT_ROOM=$(($COUNT))
    export JANUS_IN_PORT=$(($COUNT + $JANUS_START_PORT_IN - 1))
    export JANUS_IN_ROOM=$(($COUNT))
    export NUM=$COUNT;

    streaming_config=$(/bin/sh $PWD/janus.plugin.streaming.jcfg.template);
    echo $streaming_config;
    printf "%s" "$streaming_config" >> "/opt/janus/etc/janus/janus.plugin.streaming.jcfg"

    if [[ -z "${SUPERCOLLIDER_USE_INPUT}" ]]; then
        audiobridge_config=$(/bin/sh $PWD/janus.plugin.audiobridge.jcfg.template);
        printf "%s" "$audiobridge_config" >> "/opt/janus/etc/janus/janus.plugin.audiobridge.jcfg"
        # cat <<< "$audiobridge_config" >> "/opt/janus/etc/janus/janus.plugin.audiobridge.jcfg";
    fi
    COUNT=$(($COUNT + 1))
done

echo "Finshed creating configs";
