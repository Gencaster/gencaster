<template>
  <div>
    <div
      v-if="fetching"
      class="fetching-screen"
    >
      <Loading />
    </div>
    <div v-else>
      <div v-if="graphs.length > 0">
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
                @click="createNewGraph()"
              >
                <div>
                  <p>+</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <p>You're not logged in.</p>
      </div>
      <br>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { storeToRefs } from "pinia";
import { useGraphsStore } from "../stores/GraphsStore";
import Loading from "./elements/Loading.vue";

// store
const { fetching, graphs } = storeToRefs(useGraphsStore());

const createNewGraph = () => {
  alert("tbd");
};
</script>
