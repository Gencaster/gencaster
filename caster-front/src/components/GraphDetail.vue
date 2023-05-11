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
  <div><p>Landing</p></div>
</template>
