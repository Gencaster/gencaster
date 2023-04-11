<template>
  <div>
    <ElDialog
      v-model="showDialog"
      title="Careful"
      width="25%"
      center
      lock-scroll
      :show-close="false"
    >
      <span>
        Unsaved changes in the editor! <br>
        Are you sure to switch node without saving?
      </span>
      <template #footer>
        <span class="dialog-footer">
          <ElButton
            text
            bg
            @click="emit('noSave')"
          >
            Switch without saving
          </ElButton>
          <ElButton
            color="#ADFF00"
            @click="emit('cancel')"
          >
            Cancel
          </ElButton>
        </span>
      </template>
    </ElDialog>
  </div>
</template>

<script setup lang="ts">
import { ref, type Ref } from 'vue';

const emit = defineEmits<{
  (e: 'noSave'): void,
  (e: 'cancel'): void,
}>();

const showDialog: Ref<boolean> = ref(true);

</script>
