<script setup lang="ts">
import type { NodeDoor as NodeDoorType } from "@/graphql";
import NodeDoor from "@/components/NodeDoor.vue";
import { ref, type Ref } from "vue";
import DialogAddNodeDoor from "@/components/DialogAddNodeDoor.vue";

type DoorData = Pick<
  NodeDoorType,
  "code" | "doorType" | "isDefault" | "name" | "order" | "uuid"
>;

defineProps<{
  inNodeDoors: DoorData[];
  outNodeDoors: DoorData[];
  nodeUuid: string;
}>();

const showAddNodeDoorDialog: Ref<boolean> = ref(false);
</script>

<template>
  <div>
    <hr>
    <div class="node-doors">
      <h3
        v-if="inNodeDoors.length > 0"
        class="node-doors-headline"
      >
        Node Entry Doors
      </h3>
      <div
        v-if="inNodeDoors.length > 0"
        class="node-doors-in"
      >
        <NodeDoor
          v-for="nodeDoor in inNodeDoors"
          :key="nodeDoor.uuid"
          :node-door="nodeDoor"
        />
      </div>
      <h3 class="node-doors-headline">
        Node Exit Doors
      </h3>
      <ElRow
        :gutter="10"
        class="legend"
      >
        <ElCol :span="6">
          <span>Name</span>
        </ElCol>
        <ElCol :span="18">
          <span>Python</span>
        </ElCol>
      </ElRow>
      <div
        v-if="outNodeDoors.length > 0"
        class="node-doors-out"
      >
        <NodeDoor
          v-for="nodeDoor in outNodeDoors"
          :key="nodeDoor.uuid"
          :node-door="nodeDoor"
        />
        <ElRow>
          <button
            class="node-add unstyled"
            @click="
              () => {
                showAddNodeDoorDialog = true;
              }
            "
          >
            +
          </button>
        </ElRow>
      </div>
      <DialogAddNodeDoor
        v-if="showAddNodeDoorDialog"
        :node-uuid="nodeUuid"
        @closed="() => (showAddNodeDoorDialog = false)"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import "@/assets/scss/variables.module.scss";

hr {
  border-top: 1px solid $grey;
  border-bottom: 0px;
  margin-bottom: $spacingM;
}

.node-doors-headline {
  margin-bottom: $spacingM;
}

.node-doors {
  padding-left: 15px;
  padding-right: 15px;
}

.node-add {
  background-color: transparent;
  border: 1px solid $grey;
  width: 100%;
  height: 31px;
  display: flex;
  align-items: center;
  justify-content: center;

  &:hover {
    background-color: $grey-light;
  }
}

.legend {
  width: calc(100% - 25px); // same width as door
  margin-bottom: 4px;
  color: $grey-dark;
  font-size: 14px;
}
</style>
