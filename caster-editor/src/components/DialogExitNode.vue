<template>
  <div>
    <ElDialog
      v-model="showDialog"
      title="Exit node"
      center
      align-center
      lock-scroll
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <span>
        Unsaved changes in the script cells! <br>
        Are you sure to switch or exit the node without saving?
      </span>
      <template #footer>
        <span class="dialog-footer">
          <ElButton
            type="info"
            @click="emit('cancel')"
          > Cancel </ElButton>
          <ElButton
            type="danger"
            @click="emit('noSave')"
          >
            Discard changes
          </ElButton>
          <ElButton
            type="primary"
            @click="emit('save')"
          > Save </ElButton>
        </span>
      </template>
    </ElDialog>
  </div>
</template>

<script setup lang="ts">
import { ref, type Ref } from "vue";
import { ElDialog } from "element-plus";

const emit = defineEmits<{
  (e: "noSave"): void;
  (e: "save"): void;
  (e: "cancel"): void;
}>();

const showDialog: Ref<boolean> = ref(true);
</script>
