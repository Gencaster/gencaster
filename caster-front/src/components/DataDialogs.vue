<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import { storeToRefs } from "pinia";
import { ElCol, ElDialog, ElInput, ElRow } from "element-plus";
import { usePlayerStore } from "@/stores/Player";
import type { UserDataRequest } from "@/models";
const { userDataRequests, streamGPS, gpsAllowed } = storeToRefs(usePlayerStore());

const popup = computed<UserDataRequest | null>(() => {
  return userDataRequests.value[0] ?? null;
});

const showPopup = computed<boolean>(() => {
  return popup.value !== null;
});

const confirmPopup: VoidFunction = () => {
  console.log("confirm");
  userDataRequests.value.shift();
};

const gpsRequest: VoidFunction = () => {
  if (!gpsAllowed.value)
    streamGPS.value = true;
};

onMounted(() => {
  // const testPopup = {
  //   name: "Name",
  //   description: "Bitte teile uns deinen Namen mit.",
  //   key: "username",
  //   type: "string",
  //   placeholder: "Name"
  // };

  // userDataRequests.value.push(testPopup);

  // const testPopup2 = {
  //   name: "Name",
  //   description: "Drifter ist ein dynamisches Hörspiel, das in Echtzeit generiert wird. Hierfür werden noch Informationen über dich benötigt:",
  //   key: "username",
  //   type: "gps",
  //   placeholder: "Name"
  // };

  // userDataRequests.value.push(testPopup2);
});

const userData = ref<string>("");
</script>

<template>
  <div>
    <ElDialog
      v-model="showPopup"
      align-center
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <p class="description">
        {{ popup?.description }}
      </p>
      <div class="data">
        <div v-if="popup?.type === 'string'" class="component string-component">
          <ElInput v-model="userData" :placeholder="popup?.placeholder" />
        </div>
        <div v-if="popup?.type === 'gps'" class="component gps-component">
          <div class="gps-wrapper">
            <ElButton class="underline no-hover" size="default" text @click="gpsRequest()">
              <span>
                GPS Freigeben
              </span>
            </ElButton>
            <div class="checkbox" :class="{ active: gpsAllowed }" @click="gpsRequest()">
              <div v-if="gpsAllowed" class="circle" />
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <div class="confirm">
            <ElButton class="caps green" size="default" type="default" @click="confirmPopup()">
              Ok
            </ElButton>
          </div>
        </span>
      </template>
    </ElDialog>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/mixins.scss';
@import '@/assets/variables.scss';

.gps-component {
  margin-bottom: $spacingM;

  .gps-wrapper {
    display: flex;
    align-items: center;
    gap: 20px;
  }

  .checkbox {
    width: 25px;
    height: 25px;
    border: $lineStandard solid $black;
    border-radius: $borderRadius;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;

    .circle {
      background-color: $black;
      border-radius: 100%;
      width: 12px;
      height: 12px;
    }

    &.active {
      background-color: $green-light;
    }
  }
}
</style>
