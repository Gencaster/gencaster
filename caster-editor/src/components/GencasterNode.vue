<script setup lang="ts">
import { Handle, Position } from "@vue-flow/core";
import { onMounted } from "vue";
import type { Node } from "@/graphql";
import { useVueFlow } from "@vue-flow/core";

const props = defineProps<{
  data: Pick<Node, "name" | "uuid" | "inNodeDoors" | "outNodeDoors">;
}>();

const { updateNodeInternals } = useVueFlow();

onMounted(() => {
  updateNodeInternals();
});
</script>

<template>
  <div class="gencaster-node">
    <div>{{ data.name }}</div>

    <div class="in-nodes">
      <div
        v-for="inDoor in data.inNodeDoors"
        :key="inDoor.uuid"
        class="in-node"
      >
        <Handle
          :id="inDoor.uuid"
          style="background-color: red"
          type="target"
          :position="Position.Left"
        >
          <slot>
            <span style="pointer-events: none"> {{ inDoor.name }} </span>
          </slot>
        </Handle>
      </div>
    </div>

    <div class="out-nodes">
      <div
        v-for="outDoor in data.outNodeDoors"
        :key="outDoor.uuid"
        class="out-node"
      >
        <Handle
          :id="outDoor.uuid"
          :position="Position.Right"
          type="source"
          style="background-color: green; top: unset"
        >
          <slot>
            <span style="pointer-events: none"> {{ outDoor.name }} </span>
          </slot>
        </Handle>
      </div>
    </div>
  </div>
</template>

<style scoped>
.gencaster-node {
  background-color: greenyellow;
  min-height: 10vh;
  min-width: 10vw;
  display: flex;
  flex-direction: row;
  border: 1px dashed black;
}

.out-nodes {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  width: 5vw;
}

.out-node {
  height: 1vh;
  margin: 10px;
}
</style>
