<script setup lang="ts">
import { type Ref, computed, ref, watch } from "vue";
import { ElMessage } from "element-plus";
import { storeToRefs } from "pinia";
import { useRouter } from "vue-router";
import type { UserDataRequest } from "@/models";
import { usePlayerStore } from "@/stores/Player";

defineProps<{
  request: UserDataRequest
}>();

const emit = defineEmits<{
  (e: "submitted"): void
}>();

const router = useRouter();

const { streamGPS, gpsError, gpsSuccess } = storeToRefs(usePlayerStore());
const gpsAllowed: Ref<boolean> = ref(false);

const dialogVisible: Ref<boolean> = ref(true);

watch(gpsSuccess, () => {
  console.log("Received first GPS signal - connection successful");
  dialogVisible.value = false;
});

const closedDialog = () => {
  emit("submitted");
};

watch(gpsError, () => {
  if (gpsError.value) {
    console.log(`Error at obtaining GPS handle: ${gpsError.value}`, gpsError.value);
    if (gpsError.value.PERMISSION_DENIED)
      ElMessage.error("Plesae allow GPS :>");
    else if (gpsError.value.POSITION_UNAVAILABLE || gpsError.value.PERMISSION_DENIED)
      ElMessage.error(`Could not obtain a GPS position: ${gpsError.value.message}`);
    router.push("/gpsError");
  }
});

const granted: Ref<boolean> = ref(false);

const refreshIntervalId = setInterval(async () => {
  // i don't have a clue if this works properly b/c I always receive a GPS location first
  // but "in theory" it should also help us
  const { state } = await navigator.permissions.query({ name: "geolocation" });
  console.log("state is", state);
  if (state === "granted") {
    granted.value = true;
    gpsSuccess.value = true;
    clearInterval(refreshIntervalId);
  }
}, 100);

const gpsRequest = async () => {
  // as it makes only sense to have one GPS stream we refer to
  // it via the global store.
  streamGPS.value = true;
};
</script>

<template>
  <div>
    <ElDialog
      v-model="dialogVisible"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      align-center
      lock-scroll
      @closed="closedDialog()"
    >
      <p class="description">
        {{ request.description }}
      </p>
      <div class="data">
        <div class="component string-component">
          <div class="gps-wrapper">
            <ElButton class="underline no-hover" size="default" text @click="gpsRequest()">
              <span>
                GPS Freigeben
              </span>
            </ElButton>
            <ElCheckbox v-model="gpsAllowed" :disabled="gpsSuccess" @click="gpsRequest()" />
          </div>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <div class="confirm">
            <ElButton class="caps green" size="default" type="default" @click="gpsRequest()">
              Ok
            </ElButton>
          </div>
        </span>
      </template>
    </ElDialog>
  </div>
</template>
