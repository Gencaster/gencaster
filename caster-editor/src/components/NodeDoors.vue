<script setup lang="ts">
import type { NodeDoor as NodeDoorType } from "@/graphql";
import NodeDoor from "@/components/NodeDoor.vue";
import { ElButton, type ElCol } from "element-plus";
import { ref, type Ref } from "vue";
import DialogAddNodeDoor from "@/components/DialogAddNodeDoor.vue";

type DoorData = Pick<
  NodeDoorType,
  "code" | "doorType" | "isDefault" | "name" | "order" | "uuid"
>;

const props = defineProps<{
  inNodeDoors: DoorData[];
  outNodeDoors: DoorData[];
  nodeUuid: string;
}>();

const showAddNodeDoorDialog: Ref<boolean> = ref(false);
</script>

<template>
  <div class="node-doors">
    <span class="node-doors-headline">Node doors</span>
    <div
      v-if="inNodeDoors.length > 0"
      class="node-doors-in"
    >
      <span class="node-door-headline">In</span><br>
      <NodeDoor
        v-for="nodeDoor in inNodeDoors"
        :key="nodeDoor.uuid"
        :node-door="nodeDoor"
      />
    </div>
    <div
      v-if="outNodeDoors.length > 0"
      class="node-doors-out"
    >
      <span class="node-door-headline">Out</span><br>
      <NodeDoor
        v-for="nodeDoor in outNodeDoors"
        :key="nodeDoor.uuid"
        :node-door="nodeDoor"
      />
      <ElRow style="padding-top: 10px">
        <ElButton
          style="width: 100%"
          @click="
            () => {
              showAddNodeDoorDialog = true;
            }
          "
        >
          +
        </ElButton>
      </ElRow>
    </div>
    <DialogAddNodeDoor
      v-if="showAddNodeDoorDialog"
      :node-uuid="nodeUuid"
      @closed="() => (showAddNodeDoorDialog = false)"
    />
  </div>
</template>

<style scoped>
span.node-door-headline {
  background-color: lightgray;
  font-size: larger;
}

span.node-doors-headline {
  font-size: x-large;
}
</style>
