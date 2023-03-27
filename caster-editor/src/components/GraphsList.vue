<template>
  <div>
    <h1>Select one of your Graphs</h1>
    <div class="demo-control-panel">
      <div>
        <br>
        <div
          v-for="graph in graphs"
          :key="graph.uuid"
          class="graph-selection"
          :value="graph.uuid"
        >
          <router-link
            class="graph"
            :to="{ name: 'graph', params: { uuid: graph.uuid } }"
          >
            <div>
              <p>{{ graph.name }}</p>
            </div>
            <div>
              <p>{{ graph.uuid }}</p>
            </div>
          </router-link>
        </div>
        <div class="graph-selection">
          <div
            class="graph new-one"
            @click="createGraphDialogVisible = true"
          >
            <div>
              <p>+</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <AddGraph
      v-if="createGraphDialogVisible"
      @created="createGraphDialogVisible = false"
      @aborted="createGraphDialogVisible = false"
    />
  </div>
</template>

<script lang="ts" setup>
import type { Graph } from "@/graphql"
import AddGraph from "@/components/DialogAddGraph.vue";
import { ref, type Ref } from "vue";

export type GraphListType = Pick<Graph, 'name' | 'uuid'>

defineProps<{
  graphs: GraphListType[]
}>();

const createGraphDialogVisible: Ref<boolean> = ref(false);
</script>
