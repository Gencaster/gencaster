<script setup lang="ts">
import NodeEditorHeader from "@/components/NodeEditorHeader.vue";
import NodeEditorCells from "./NodeEditorCells.vue";
import { useNodeSubscription } from "@/graphql";
import { computed, watch, type Ref, toRef } from "vue";
import { useInterfaceStore } from "@/stores/InterfaceStore";
import { storeToRefs } from "pinia";
import { ElMessage } from "element-plus";

const props = defineProps<{
  uuid: string;
}>();

const refUuid: Ref<string> = toRef(props, "uuid");

const { waitForScriptCellsUpdate, newScriptCellUpdates, cachedNodeData } =
  storeToRefs(useInterfaceStore());

const { data, error } = useNodeSubscription(
  {
    variables: {
      // some "bug"(?) in vue - otherwise prop is not updating
      uuid: refUuid,
    },
    pause: computed(() => newScriptCellUpdates.value.size > 0),
  },
  (messages, response) => {
    // callback on receiving an update from subscription
    console.log("Received node update", response);
    waitForScriptCellsUpdate.value = false;
    cachedNodeData.value = response;
    return response;
  },
);

watch(error, (x) => {
  ElMessage.error(`Problems receiving node update: ${x?.message}`);
});
</script>

<template>
  <div
    v-loading="!data || waitForScriptCellsUpdate || data.node.uuid != refUuid"
    class="node-editor"
  >
    <NodeEditorHeader
      v-if="data"
      :node="data.node"
    />
    <div class="editor-header-spacer" />
    <NodeEditorCells
      v-if="cachedNodeData"
      v-model:script-cells="cachedNodeData.node.scriptCells"
    />
  </div>
</template>

<style lang="scss" scoped>
@import "@/assets/scss/variables.module.scss";
.node-editor {
  z-index: 2;
  background-color: white;
  position: fixed;
  width: 800px;
  height: calc(100vh - 100px);
  right: 10px;
  top: 80px;
  transition: right 0.3s ease-in-out;
  overflow-x: hidden;
  border: 1px solid $black;
}

.editor-header-spacer {
  width: inherit;
  height: calc($menuHeight * 2);
  margin-bottom: 30px;
}
</style>
