<template>
  <div>
    <button
      class="unstyled"
      @click="directLink()"
    >
      Public
    </button>
    <button
      class="unstyled"
      @click="debug()"
    >
      Debug
    </button>
  </div>
</template>

<script setup lang="ts">
import type { Graph } from "@/graphql";
import { ElMessage } from "element-plus";

const props = defineProps<{
  graph: Pick<Graph, "uuid" | "slugName">;
}>();

const gencasterFrontUrl = (): string | undefined => {
  // see https://github.com/Gencaster/gencaster/pull/552/files#r1315599653
  let url: string | undefined = undefined;
  if (window.location.host === "127.0.0.1") {
    url = "http://127.0.0.1:3000";
  } else if (import.meta.env.GENCASTER_FRONT_URL) {
    url = import.meta.env.GENCASTER_FRONT_URL;
  }
  return url;
};

const directLink = () => {
  const frontUrl = gencasterFrontUrl();
  if (frontUrl) {
    window.open(`${frontUrl}/listen/${props.graph.slugName}`, "_blank");
  } else {
    ElMessage.error(`Could not find the URL for the Gencaster frontend`);
  }
};

const debug = () => {
  const frontUrl = gencasterFrontUrl();
  if (frontUrl) {
    window.open(`${frontUrl}/debug`, "_blank");
  } else {
    ElMessage.error(`Could not find the URL for the Gencaster frontend`);
  }
};
</script>
