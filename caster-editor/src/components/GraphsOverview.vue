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
                @click="createGraphDialogVisible = true"
              >
                <div>
                  <p>+</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <ElDialog
          v-model="createGraphDialogVisible"
          width="25%"
          title="Create graph"
          :show-close="false"
        >
          <ElInput
            id="graphNameInput"
            v-model="newGraphDialogName"
            placeholder="Name of graph"
          />
          <template #footer>
            <span class="dialog-footer">
              <ElButton @click="createGraphDialogVisible = false">Cancel</ElButton>
              <ElButton
                color="#ADFF00"
                type="primary"
                @click="createGraph()"
              >
                Confirm
              </ElButton>
            </span>
          </template>
        </ElDialog>
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
import { ElDialog } from "element-plus";
import Loading from "./elements/Loading.vue";
import { ref, type Ref } from "vue";

// store
const graphsStore = useGraphsStore();
const { fetching, graphs } = storeToRefs(graphsStore);

const createGraphDialogVisible: Ref<boolean> = ref(false);
const newGraphDialogName: Ref<string> = ref("");

const createGraph = async() => {
  const error = await graphsStore.createGraph({name: newGraphDialogName.value});
  if(error!==undefined) {
    alert("Could not create graph: " + error);
    return;
  }
  createGraphDialogVisible.value=false;
  newGraphDialogName.value = "";
}

</script>
