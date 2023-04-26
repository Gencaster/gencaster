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

<style lang="scss" scoped>
@import '@/assets/scss/variables.module.scss';

.graph-selection {
    .graph {
      width: 100%;
      height: 50px;
      background-color: $mainWhite;
      border: 1px solid $mainBlack;
      border-bottom: 0;
      display: flex;
      justify-content: space-between;
      text-decoration: none;

      div {
        padding-left: $globalPadding;
        padding-right: $globalPadding;
        width: auto;
        display: flex;
        align-items: center;
        p {
          margin: 0;
        }
      }

      &:hover {
        background-color: $hoverColor;
        cursor: pointer;
      }

      &.new-one {
        text-align: center;
        border: 1px solid $mainBlack;
        div {
          width: 100%;
          p {
            width: inherit;
            text-align: center;
          }
        }
      }
    }
  }

</style>
