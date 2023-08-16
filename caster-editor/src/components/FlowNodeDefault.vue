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

const isValidConnection = (connection: any) => {
  // console.log(connection.targetHandle === "a");
  // return connection.targetHandle === "a";
  return true;
};
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
      :position="Position.Left"
      :style="sourceHandleStyleA"
    />

    <Handle
      id="b"
      type="source"
      :position="Position.Right"
      :style="sourceHandleStyleB"
      :is-valid-connection="isValidConnection"
    />
  </div>
</template>

<style lang="scss" scoped>
@import "@/assets/scss/variables.module.scss";

.node {
  padding: 10px;
  border-radius: 4px;
  height: auto;
  width: 160px;
  // border: 1px solid black;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  min-height: 50px;

  p {
    text-align: center;
    height: 100%;
    margin: 0;
  }
}
</style>
