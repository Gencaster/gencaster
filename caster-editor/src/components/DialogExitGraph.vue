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
        Are you sure to exit without saving? <br>
        Some of your changes might get lost.
      </span>
      <template #footer>
        <span class="dialog-footer">
          <ElButton
            text
            bg
            @click="() => {emit('cancel')}"
          >Cancel</ElButton>
          <ElButton
            color="#FF0000"
            @click="exitGraph()"
          >
            Exit
          </ElButton>
        </span>
      </template>
    </ElDialog>
  </div>
</template>

<script setup lang="ts">
import { ref, type Ref } from 'vue';
import { useRouter } from "vue-router";

const router = useRouter();
const emit = defineEmits<{
    (e: 'cancel'): void
}>();


const showDialog: Ref<boolean> = ref(true);

const exitGraph = () => {
    showDialog.value = false;
    router.push({
        path: "/graph",
    });
}

</script>
