<template>
  <div>
    <p>toto</p>
    <p>{{ uuid }}</p>

    <div v-if="isFetching">
      Loading
    </div>

    <div v-else>
      {{ graph }}
    </div>
  </div>
</template>

<script lang="ts">
import type { Ref } from "vue";
import { computed, defineComponent, ref } from "vue";
import type { AnyVariables, UseQueryState } from "@urql/vue";
import type { GetGraphQuery, Graph } from "@/graphql/graphql";
import { useGetGraphQuery } from "@/graphql/graphql";
import { createError } from "#app";

export default defineComponent({
  props: {
    uuid: {
      type: String,
      required: true
    }
  },

  async setup(props) {
    console.log(props);
    const result: Ref<UseQueryState<GetGraphQuery, AnyVariables> | undefined> = ref(undefined);
    result.value = await useGetGraphQuery({
      variables: { uuid: props.uuid },
      requestPolicy: "network-only"
    });

    if (!result.value) {
      throw createError({
        statusCode: 404,
        statusMessage: "Page Not Found"
      });
    }
    console.log(result);
    // console.log(data?.graph);
    // if (!data.gr) {
    //   console.log("error");
    // }
    // ;

    const graph: Graph | undefined = result.value.data.value?.graph;
    const isFetching = computed(() => result.value.fetching);

    return {
      isFetching,
      graph
    };
  }
});
</script>
