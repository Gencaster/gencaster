<script lang="ts" setup>
import { Handle, Position } from "@vue-flow/core";
import { computed } from "vue";

interface DataInput {
  name: {
    type: String;
    required: true;
  };
  uuid: {
    type: String;
    required: true;
  };
  scriptCells: {
    type: Array;
    required: true;
  };
}

const props = defineProps({
  //TODO: needs to be typed correctly
  data: {
    type: Object as PropType<DataInput>,
    required: true,
  },
});

const emit = defineEmits(["dblclick"]);

function onDblClick() {
  // console.log(`dblclicked ${props.data.uuid}`);
  emit("dblclick", props.data.uuid);
}

const sourceHandleStyleA = computed(() => ({
  backgroundColor: "red",
  width: "10px",
  height: "10px",
}));

const sourceHandleStyleB = computed(() => ({
  backgroundColor: "blue",
  width: "10px",
  height: "10px",
}));
</script>

<template>
  <div
    class="node default-node"
    @dblclick="onDblClick"
  >
    <p>{{ data.name }}</p>

    <Handle
      id="a"
      type="target"
      :position="Position.Top"
      :style="sourceHandleStyleA"
    />

    <Handle
      id="b"
      type="source"
      :position="Position.Bottom"
      :style="sourceHandleStyleB"
    />
  </div>
</template>

<style lang="scss" scoped>
@import "@/assets/scss/variables.module.scss";

.node {
  padding: 10px;
  border-radius: 4px;
  height: auto;
  background-color: yellow;
  width: 200px;
  border: 1px solid black;
}
</style>
