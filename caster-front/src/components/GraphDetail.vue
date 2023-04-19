<!-- eslint-disable vue/attribute-hyphenation -->
<script setup lang="ts">
import { useRouter } from "vue-router";
import { useGetGraphsQuery } from "@/graphql";
import GraphPlayer from "@/components/GraphPlayer.vue";

const props = defineProps<{
  graphName: string
  fullView: Boolean
}>();

const router = useRouter();

const { data, fetching, error } = useGetGraphsQuery({
  variables: {
    name: props.graphName
  }
});
</script>

<template>
  <div v-if="router.currentRoute.value.name === 'graphPlayer'" v-loading="fetching" class="graph-detail">
    <div v-if="error || (!fetching && (data?.graphs.length !== 1)) || !data" class="error">
      Could not find proper graph
    </div>
    <div v-else>
      <GraphPlayer
        :graph="data.graphs[0]"
      />
    </div>
  </div>
</template>
