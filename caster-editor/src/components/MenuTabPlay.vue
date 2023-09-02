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
export type GraphEdit = Pick<Graph, "uuid" | "slugName">;

const props = defineProps<{
  graph: GraphEdit;
}>();

const directLink = () => {
  // https://editor.dev.gencaster.org/graph/c5408723-7a2d-4111-826c-9ec507c0b65e
  // to https://dev.gencaster.org/listen/demo/

  if (import.meta.env.DEV) {
    const newUrl = "http://127.0.0.1:3000/listen/" + props.graph.slugName;
    window.open(newUrl, "_blank");
  } else {
    const host = window.location.host;
    const newUrl = "https://" + host + "/listen/" + props.graph.slugName;
    window.open(newUrl, "_blank");
  }
};

const debug = () => {
  if (import.meta.env.DEV) {
    const newUrl = "http://127.0.0.1:3000/debug";
    window.open(newUrl, "_blank");
  } else {
    const host = window.location.host;
    const newUrl = "https://" + host + "/debug/";
    window.open(newUrl, "_blank");
  }
};
</script>
