<script setup lang="ts">
import { ElDialog } from "element-plus";
import { type Ref, ref } from "vue";
import type { UserDataRequest } from "@/models";
import { UserDataRequestType } from "@/models";
import GpsDialog from "@/components/Dialogs/GpsDialog.vue";
import NameDialog from "@/components/Dialogs/NameDialog.vue";
import type { Scalars } from "@/graphql";

defineProps<{
  request: UserDataRequest
  streamUuid: Scalars["UUID"]
}>();

const emit = defineEmits<{
  (e: "submitted"): void
}>();
</script>

<template>
  <div>
    <div>
      <NameDialog
        :stream-uuid="streamUuid"
        :request="request"
        @submitted="() => $emit('submitted')"
      />
    </div>
    <div v-if="request.type === UserDataRequestType.Gps">
      <GpsDialog
        :request="request"
      />
    </div>
  </div>
</template>
