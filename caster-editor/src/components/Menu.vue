<template>
  <div>
    <div class="menu menu-edit">
      <div class="level level-1">
        <div class="menu-items left">
          <ElRadioGroup v-model="menuStore.tab">
            <ElRadioButton :label="Tab.Edit">
              Build
            </ElRadioButton>
            <ElRadioButton :label="Tab.Play">
              Listen
            </ElRadioButton>
          </ElRadioGroup>
        </div>
        <div class="menu-items middle">
          <span>
            {{ graphInStore?.graph.name }}
          </span>
        </div>
        <div class="menu-items right">
          <button
            class="unstyled"
            @click="exitWithoutSaving()"
          >
            Exit
          </button>
        </div>
      </div>
      <div class="level level-2">
        <div
          v-if="menuStore.tab === Tab.Edit"
          class="left"
        >
          <button
            class="unstyled"
            @click="addNode()"
          >
            Add Scene
          </button>
          <button
            class="unstyled"
            :class="{ lighter: hideConnectionButton }"
            @click="createEdge()"
          >
            Add Connection
          </button>
          <button
            class="unstyled"
            :class="{ lighter: hideRemoveButton }"
            @click="removeSelection()"
          >
            Remove
          </button>
          <!-- TODO: Rewrite a reloadfromserver function -->
          <button class="unstyled">
            Refresh
          </button>
        </div>
        <div v-if="menuStore.tab === Tab.Play" />
      </div>
    </div>
    <div class="menu-spacer" />

    <!-- Dialogs -->
    <!-- Are you sure to delete? -->
    <ElDialog
      v-model="deleteDialogVisible"
      title="Careful"
      width="25%"
      center
      lock-scroll
      :show-close="false"
    >
      <span>
        Are you sure to delete Scene "{{ selectedNodeName }}"?
      </span>
      <template #footer>
        <span class="dialog-footer">
          <ElButton
            text
            bg
            @click="deleteDialogVisible = false"
          >Cancel</ElButton>
          <ElButton
            color="#FF0000"
            @click="deleteSelectedNodes()"
          >
            Delete Node
          </ElButton>
        </span>
      </template>
    </ElDialog>

    <!-- Exit Page -->
    <ElDialog
      v-model="exitDialogVisible"
      title="Careful"
      width="25%"
      center
      lock-scroll
      :show-close="false"
    >
      <span>
        Are you sure to exit without saving? <br>
        Some of your changes might get lost.
      </span>
      <template #footer>
        <span class="dialog-footer">
          <ElButton
            text
            bg
            @click="exitDialogVisible = false"
          >Cancel</ElButton>
          <ElButton
            color="#FF0000"
            @click="exitWithoutSaving()"
          >
            Exit
          </ElButton>
        </span>
      </template>
    </ElDialog>
  </div>
</template>

<script lang="ts" setup>
export interface MenuProps {
  graph?: GraphInstance;
  uuid: Scalars["UUID"];
  selectedNodes: string[];
  selectedEdges: string[];
}

import { storeToRefs } from "pinia";
import type { Instance as GraphInstance } from "v-network-graph";
import type { Scalars } from "@/graphql";
import { ElButton, ElMessage, ElRadioButton, ElRadioGroup } from "element-plus";
import { Tab, useMenuStore } from "@/stores/MenuStore";
import { useRouter } from "vue-router";
import { computed, ref } from "vue";
import { useGraphStore } from "@/stores/GraphStore";

// Props
const props = defineProps<MenuProps>();

// Store
const menuStore = useMenuStore();
const graphStore = useGraphStore();
const { graph: graphInStore } = storeToRefs(graphStore);

// Composables
const router = useRouter();

// Computed
const hideConnectionButton = computed(() => {
  return props.selectedNodes.length !== 2;
});

const selectedNodeName = computed(() => {
  const nodeUuid = props.selectedNodes[0] || ""
  let name = "undefined"
  graphInStore.value?.graph.nodes.forEach(node => {
    if (node.uuid === nodeUuid) {
      name = node.name
    }
  });

  return name
})

const hideRemoveButton = computed(() => {
  if (
    (props.selectedNodes.length === 0 && props.selectedEdges.length === 0) ||
    (props.selectedNodes.length === 0 && props.selectedEdges.length === 0)
  )
    return true;
  else if (props.selectedNodes.length > 1 || props.selectedEdges.length > 1)
    return true;
  else return false;
});

// Interface
const deleteDialogVisible = ref(false);
const exitDialogVisible = ref(false);

const exitWithoutSaving = () => {
  router.push({
    path: "/graphs",
  });
};

// functions
const addNode = async () => {
  if (!props.graph) {
    console.error("can't add node since graph not defined", props.graph);
    return;
  }

  const { height, width } = props.graph.getSizes();
  const centerPosition = props.graph.translateFromDomToSvgCoordinates({
    x: width / 2,
    y: height / 2,
  });

  await graphStore.addNode({
    graphUuid: props.uuid,
    name: "new scene",
    color: "primary",
    positionX: centerPosition.x,
    positionY: centerPosition.y,
  });
};

const createEdge = async () => {
  if (props.selectedNodes.length !== 2) {
    ElMessage({
      message: "requires exactly 2 scenes selected.",
      type: "error",
      customClass: "messages-editor",
    });
    return;
  }
  const [source, target] = props.selectedNodes;
  await graphStore.createEdge(source, target);
};

const deleteSelectedNodes = async () => {
  deleteDialogVisible.value = false;
  // work on a copy to not get into problems
  for (const nodeUuid of [...props.selectedNodes])
    await graphStore.deleteNode(nodeUuid);
};

const deleteSelectedEdges = async () => {
  for (const edgeUuid of props.selectedEdges)
    await graphStore.deleteEdge(edgeUuid);
};

const removeSelection = () => {
  // check if only one type is selected
  // right now we only allow one element deletion
  // TODO: needs to check if the async call is not buggy if looping through
  if (props.selectedNodes.length === 1 && props.selectedEdges.length === 0) {
    deleteDialogVisible.value = true;
  } else if (
    props.selectedNodes.length === 0 &&
    props.selectedEdges.length === 1
  ) {
    deleteSelectedEdges();
  } else {
    ElMessage({
      message: "Please select max one scene or one connection.",
      type: "error",
      customClass: "messages-editor",
    });
  }
};
</script>
