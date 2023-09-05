<template>
  <div>
    <ElDialog
      v-model="showDialog"
      title="Careful"
      center
      lock-scroll
      :show-close="false"
      align-center
    >
      <span>
        Are you sure to exit the graph?
        <span v-if="newScriptCellUpdates.size > 0">
          <br><b>There are unsaved changes in the Node-Editor.</b>
        </span>
      </span>
      <template #footer>
        <span class="dialog-footer">
          <ElButton
            type="info"
            @click="
              () => {
                emit('cancel');
              }
            "
          >Cancel</ElButton>
          <ElButton
            type="danger"
            @click="exitGraph()"
          > Exit </ElButton>
        </span>
      </template>
    </ElDialog>
  </div>
</template>

<script setup lang="ts">
import { useInterfaceStore } from "@/stores/InterfaceStore";
import { storeToRefs } from "pinia";
import { ref, type Ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const emit = defineEmits<{
  (e: "cancel"): void;
}>();

const interfaceStore = useInterfaceStore();
const { selectedNodeForEditorUuid, newScriptCellUpdates } =
  storeToRefs(interfaceStore);

const showDialog: Ref<boolean> = ref(true);

const exitGraph = () => {
  showDialog.value = false;

  selectedNodeForEditorUuid.value = undefined;
  interfaceStore.resetUpdates();

  router.push({
    path: "/graph",
  });
};
</script>
