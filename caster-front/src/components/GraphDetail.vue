<!-- eslint-disable vue/attribute-hyphenation -->
<script setup lang="ts">
import { useRouter } from "vue-router";
import { useGetGraphsQuery } from "@/graphql";
import DefaultDetail from "@/components/GraphDetailTemplates/Default.vue";
import DrifterDetail from "@/components/GraphDetailTemplates/Drifter.vue";

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
    <!-- @todo use a database field here -->
    <div v-else-if="data?.graphs[0].name.includes('Drifter')">
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

<style lang="scss" scoped>
@import '@/assets/variables.scss';
// .graph-detail {
//   margin: 0 auto;
//   width: calc(100% - 2 * $mobilePadding);
// }
</style>
