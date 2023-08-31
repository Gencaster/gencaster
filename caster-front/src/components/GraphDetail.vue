<script setup lang="ts">
import { useRouter } from "vue-router";
import { GraphDetailTemplate, useGetGraphsMetaQuery } from "@/graphql";
import DefaultDetail from "@/components/GraphDetailTemplates/DefaultTemplate.vue";
import { ref } from "vue";

const props = defineProps<{
  graphSlug: string;
  fullView: Boolean;
}>();

const router = useRouter();

const { data, fetching, error } = useGetGraphsMetaQuery({
  variables: {
    slug: props.graphSlug,
  },
});

const loadingDebounced = ref(false);

setTimeout(() => {
  loadingDebounced.value = true;
}, 1500);
</script>

<template>
  <div
    v-if="router.currentRoute.value.name === 'graphPlayer'"
    class="graph-detail"
  >
    <div
      v-if="error || (!fetching && data?.graphs.length !== 1) || !data"
      class="error general-padding"
    >
      <div v-if="loadingDebounced">
        <p>
          Could not find proper graph <br>
          In case this error persists, please contact us
          <a href="mailto:contact@gencaster.org">here</a>.
        </p>
      </div>
    </div>
    <div
      v-else-if="data?.graphs[0].templateName === GraphDetailTemplate.Default"
    >
      <DefaultDetail :graph="data.graphs[0]" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import "@/assets/mixins.scss";
@import "@/assets/variables.scss";
.graph-detail {
  min-height: 100vh;
  max-height: 100vh;
}
</style>
