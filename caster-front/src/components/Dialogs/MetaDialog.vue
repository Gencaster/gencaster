<script setup lang="ts">
import type { UserDataRequest } from "@/models";
import { UserDataRequestType } from "@/models";
import GpsDialog from "@/components/Dialogs/GpsDialog.vue";
import StringDialog from "@/components/Dialogs/StringDialog.vue";
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
    <div v-if="request.type === UserDataRequestType.String">
      <StringDialog
        :stream-uuid="streamUuid"
        :request="request"
        @submitted="() => $emit('submitted')"
      />
    </div>
    <div v-if="request.type === UserDataRequestType.Gps">
      <GpsDialog
        :request="request"
        @submitted="() => $emit('submitted')"
      />
    </div>
  </div>
</template>
