<script lang="ts" setup>
import { storeToRefs } from "pinia";
import { type Ref, ref, watch } from "vue";
import { usePlayerStore } from "@/stores/Player";
import type { Scalars, StreamVariableInput } from "@/graphql";
import { useSendStreamVariableMutation } from "@/graphql";

const { streamInfo } = storeToRefs(usePlayerStore());

const sendStreamVariableMutation = useSendStreamVariableMutation();

const stream: Ref<boolean> = ref(false);
const watcherId: Ref<number | undefined> = ref(undefined);
const sendNull: Ref<boolean> = ref(false);

const startStreaming = () => {
  console.log("Start GPS streaming");

  navigator.geolocation.getCurrentPosition((position) => {
    console.log("New position ", position);
    let streamUuid: Scalars["UUID"];
    if (streamInfo.value?.streamInfo.__typename === "StreamInfo") {
      streamUuid = streamInfo.value.streamInfo.stream.uuid;
    }
    else {
      console.log("Could not retrieve current stream UUID for GPS streaming");
      return;
    }
    const streamVariables: StreamVariableInput[] = [];

    // hacky but somehow we can not access the interface via .keys or .entries
    ["longitude", "latitude", "speed", "accuracy", "heading", "altitude", "altitudeAccuracy"].forEach((k) => {
      // @ts-expect-error 7053: ts does not like to access the attributes via strings?
      const v: any = position.coords[k];
      if ((v === null) && !sendNull.value)
        return;

      streamVariables.push({
        streamUuid,
        key: k,
        value: String(v),
        streamToSc: !isNaN(v)
      });
    });

    if (streamVariables.length > 0)
      sendStreamVariableMutation.executeMutation({ streamVariables });
  });
};

const stopStreaming = () => {
  console.log("Stop GPS streaming");
  if (watcherId.value)
    navigator.geolocation.clearWatch(watcherId.value);
};

watch(stream, () => {
  stream.value ? startStreaming() : stopStreaming();
});
</script>

<template>
  <el-button
    class="button"
    type="warning"
    @click="() => stream = !stream"
  >
    {{ stream ? "Disable" : "Activate" }} GPS streaming
  </el-button>
</template>
