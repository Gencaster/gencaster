<script setup lang="ts">
import { useRouter } from "vue-router";
import { GraphDetailTemplate, useGetGraphsMetaQuery } from "@/graphql";
import DefaultDetail from "@/components/GraphDetailTemplates/DefaultTemplate.vue";
import DrifterDetail from "@/components/GraphDetailTemplates/DrifterTemplate.vue";

const props = defineProps<{
  graphSlug: string
  fullView: Boolean
}>();

const router = useRouter();

const { data, fetching, error } = useGetGraphsMetaQuery({
  variables: {
    slug: props.graphSlug,
  },
});
</script>

<template>
  <div
    v-if="router.currentRoute.value.name === 'graphPlayer'"
    v-loading="fetching"
    class="graph-detail"
  >
    <div
      v-if="error || (!fetching && (data?.graphs.length !== 1)) || !data"
      class="error"
    >
      Could not find proper graph
    </div>
    <div v-else-if="data?.graphs[0].templateName === GraphDetailTemplate.Drifter">
      <DrifterDetail
        :graph="data.graphs[0]"
      />
    </div>
    <div v-else>
      <DefaultDetail
        :graph="data.graphs[0]"
      />
    </div>
  </div>
</template>
