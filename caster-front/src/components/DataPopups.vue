<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import { storeToRefs } from "pinia";
import { ElInput } from "element-plus";
import { usePlayerStore } from "@/stores/Player";
import type { UserDataRequest } from "@/models";
const { userDataRequests, streamGPS, gpsAllowed } = storeToRefs(usePlayerStore());

const popup = computed<UserDataRequest | null>(() => {
  return userDataRequests.value[userDataRequests.value.length - 1] ?? null;
});

const confirmPopup = () => {
  console.log("confirm");
};

const gpsRequest = () => {
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
    <div class="wrapper fullscreen-wrapper-fixed">
      <Transition>
        <div v-if="popup" class="popup">
          <p class="description">
            {{ popup?.description }}
          </p>
          <div class="data">
            <div v-if="popup?.type === 'string'" class="component string-component">
              <ElInput v-model="userData" :placeholder="popup?.placeholder" />
            </div>
            <div v-if="popup?.type === 'gps'" class="component gps-component">
              <div class="flex">
                <button class="text-btn text-btn-medium underline" @click="gpsRequest()">
                  GPS Freigeben
                </button>
                <div class="checkbox" :class="{ active: gpsAllowed }" @click="gpsRequest()">
                  <div v-if="gpsAllowed" class="circle" />
                </div>
              </div>
            </div>
          </div>
          <div class="confirm">
            <ElButton class="caps green" size="default" type="default" @click="confirmPopup()">
              Ok
            </ElButton>
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/mixins.scss';
@import '@/assets/variables.scss';

.wrapper {
  pointer-events: none;

  .popup {
    pointer-events: auto;
    margin: 0 auto;
    position: relative;
    display: block;
    box-sizing: border-box;
    border-radius: $borderRadius;
    border: $lineStandard solid $black;
    padding: 20px;
    padding-top: 0;
    background-color: $white;
    width: calc(100% - 2 * $mobilePadding);
    max-width: $cardMaxWidth;

    height: auto;
    // min-height: 300px;
    max-height: calc(70vh - 4 * $mobilePadding);
    overflow-y: scroll;
  }

  .description {
    @include fontStyle('smallHeadline');
    margin-top: $spacingM;
    margin-bottom: $spacingM;
  }

  .data {
    width: 100%;

  }

  .confirm {
    display: flex;
    justify-content: flex-end;
    margin-top: $spacingM;

  }

  .component {
    @include fontStyle('smallHeadline');
  }

  .gps-component {
    margin-bottom: $spacingM;

    .checkbox {
      width: 25px;
      height: 25px;
      border: $lineStandard solid $black;
      border-radius: $borderRadius;
      display: flex;
      justify-content: center;
      align-items: center;

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

  .flex {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

}
</style>
