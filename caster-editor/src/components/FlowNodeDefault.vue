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
  <div class="gencaster-default-node">
    <div class="title">
      <p>
        {{ data.name }}
      </p>
    </div>

    <div class="nodes">
      <div class="in-nodes">
        <div
          v-for="(inDoor, index) in data.inNodeDoors"
          :key="inDoor.uuid"
          class="in-node"
        >
          <Handle
            :id="inDoor.uuid"
            class="handle"
            :position="Position.Left"
            :style="'top: ' + (index * 24 + 42) + 'px' + '; left: -6px'"
            type="target"
          >
            <!-- <slot>
              <span style="pointer-events: none"> {{ inDoor.name }} </span>
            </slot> -->
          </Handle>
        </div>
      </div>

      <div
        class="out-nodes"
        :style="'height: ' + data.outNodeDoors.length * 24 + 'px'"
      >
        <div
          v-for="(outDoor, index) in data.outNodeDoors"
          :key="outDoor.uuid"
          class="out-node"
        >
          <Handle
            :id="outDoor.uuid"
            class="handle"
            :position="Position.Right"
            :style="'top: ' + (index * 24 + 42) + 'px' + '; right: -6px'"
            type="source"
          >
            <slot>
              <span style="pointer-events: none"> {{ outDoor.name }} </span>
            </slot>
          </Handle>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import "@/assets/scss/variables.module.scss";
.gencaster-default-node {
  background-color: $white;
  min-height: 55px;
  height: auto;
  width: $nodeDefaultWidth;
  display: flex;
  flex-direction: column;
  border: 1px solid $mainBlack;

  .title {
    background-color: $grey-light;
    height: 24px;
    padding: 2px 8px 0 8px;
    margin: 0;
  }
}

.handle {
  width: 12px;
  height: 12px;
  border-radius: 12px;
  border: 1px solid $mainBlack;
  background-color: $grey-light;
}

.out-nodes {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  width: 100px;
  margin-bottom: 12px;

  .out-node {
    span {
      position: absolute;
      text-align: right;
      pointer-events: none;
      right: 0;
      height: 20px;
      width: calc($nodeDefaultWidth - 24px);
      transform: translateX(-16px) translateY(-5px);
      text-overflow: ellipsis;
      overflow: hidden;
      white-space: nowrap;
    }
  }
}
</style>
