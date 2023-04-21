<script lang="ts" setup>
import { storeToRefs } from "pinia";
import { computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import Graph from "@/components/Graph.vue";
import Menu from "@/components/Menu.vue";
import NodeEditor from "@/components/NodeEditor.vue";
import { useInterfaceStore } from "@/stores/InterfaceStore";
import { useCreateUpdateScriptCellsMutation, useGraphSubscription, useNodeSubscription, type NodeSubscription, type ScriptCellInput } from "@/graphql"
import { ElMessage } from "element-plus";

const { showNodeEditor, selectedNodeUUIDs, scriptCellsModified } = storeToRefs(useInterfaceStore());

const router = useRouter();
const route = useRoute();

const graphSubscription = useGraphSubscription({
  variables: {
    uuid: route.params.uuid,
  },
  pause: route.params.uuid === undefined
});

const nodeSubscription = useNodeSubscription({
  variables: {
    uuid: computed(() => {console.log(`New uuid is ${selectedNodeUUIDs.value}`); return selectedNodeUUIDs.value[0]})
  },
  pause: computed(() => selectedNodeUUIDs.value.length==0 && scriptCellsModified.value),
});

watch(graphSubscription.error, () => {
  if (graphSubscription.error.value?.name === 'CombinedError') {
    alert("Accessed unknown graph - redirect to graph selection");
    router.push("/graph");
  }
});

const nodeData = computed<NodeSubscription['node'] | undefined>({
  get() {
    return nodeSubscription.data.value?.node
  },
  set(value) {
    if(value && nodeSubscription.data.value?.node) {
      nodeSubscription.data.value.node = value;
    }
    return value;
  }
});

const scriptCellMutation = useCreateUpdateScriptCellsMutation();

const saveNode = async () => {
  console.log("I should now save the node");
  if(!nodeData.value) {
    return;
  }
  // this needs to be rewritten - some types between DOM and
  // input do not add up, therefore we need to translate the data here
  const scriptCellInputs: ScriptCellInput[] = nodeData.value.scriptCells.map((domCell) => {
    const input: ScriptCellInput = {
      'uuid': domCell.uuid,
      'cellCode': domCell.cellCode,
      'cellOrder': domCell.cellOrder,
      'cellType': domCell.cellType,
    };
    if(domCell.audioCell) {
      input['audioCell'] = {
        'volume': domCell.audioCell.volume,
        'uuid': domCell.audioCell.uuid,
        'playback': domCell.audioCell.playback,
        'audioFile': {
          'uuid': domCell.audioCell.audioFile.uuid
        }
      }
    }
    return input;
  });

  const {error} = await scriptCellMutation.executeMutation({
    nodeUuid: nodeData.value.uuid,
    scriptCellInputs: scriptCellInputs
  });

  if(error) {
    ElMessage.error(`Could not save Script Cell: ${error.message}`);
  } else {
    scriptCellsModified.value = false;
  }
};
</script>

<template>
  <div
    v-if="graphSubscription.data.value"
    class="edit-page"
  >
    <Menu
      :graph="graphSubscription.data.value.graph"
    />

    <Graph
      :graph="graphSubscription.data.value.graph"
    />

    <NodeEditor
      v-if="showNodeEditor && nodeData"
      v-model:node="nodeData"
      class="node-editor-outer"
      @save-node="saveNode()"
    />
  </div>
  <div
    v-else
  >
    Failed to fetch data
  </div>
</template>
