<script setup lang="ts">
import { Plus, Scissor, VideoPause, VideoPlay } from "@element-plus/icons-vue";
</script>

<template>
  <div class="index-page">
    <div>
      <div class="menu menu-edit">
        <div class="level level-1">
          <div class="menu-items left">
            <el-radio-group v-model="menuLevel1">
              <el-radio-button label="edit">
                Edit
              </el-radio-button>
              <el-radio-button label="test">
                Test
              </el-radio-button>
              <el-radio-button label="dev">
                Dev
              </el-radio-button>
            </el-radio-group>
          </div>
          <div class="menu-items middle">
            <span v-if="fetching">
              Loading ...
            </span>
            <span v-if="!fetching">
              {{ graphData.name }}
            </span>
          </div>
          <div class="menu-items right">
            <button class="unstyled state" @click="saveState()">
              <div class="state-indicator" :class="{ saved: stateSaved }" />
              Save
            </button>

            <button class="unstyled" @click="exitEditing()">
              Exit
            </button>
          </div>
        </div>
        <div class="level level-2">
          <div v-if="menuLevel1 === 'edit'" class="left">
            <button class="unstyled" @click="addNode()">
              Add Node
            </button>
            <!-- <button class="unstyled" :disabled="selectedNodes.length !== 2" @click="addEdge()"> -->
            <button class="unstyled" :class="{ lighter: hideConnectionButton }" @click="addEdge()">
              Add Connection
            </button>
            <button class="unstyled" :class="{ lighter: hideRemoveButton }" @click="removeAny()">
              Remove
            </button>
            <button class="unstyled" @click="refresh()">
              Refresh
            </button>
          </div>
          <div v-if="menuLevel1 === 'test'" />
        </div>
      </div>
      <div class="menu-spacer" />
    </div>
    <div v-if="fetching">
      <elementsLoading />
    </div>
    <div v-if="fetchedOnce">
      <v-network-graph
        v-model:selected-nodes="selectedNodes" v-model:selected-edges="selectedEdges" class="graph"
        :nodes="nodes" :edges="edges" :configs="configs" :layouts="layouts" :event-handlers="eventHandlers"
      />

      <p v-if="showGraphData">
        {{ nodes }}
        <br>
        {{ layouts }}
        <br>
        {{ graphData }}
        <!-- {{ graphData }} -->
      </p>

      <div v-if="showNodeData" class="node-data">
        <ElementsBlockEditor :current-node-name="currentNodeName" :blocks-data="selectedNodeScriptCells" />
      </div>

      <div v-if="!showNodeData" class="stats">
        <p>
          Nodes: {{ graphData.nodes.length }} &nbsp;
          Edges: {{ graphData.edges.length }}
        </p>
      </div>

      <!-- Dialogs -->
      <!-- Exit Page -->
      <el-dialog v-model="exitDialogVisible" title="Careful" width="25%" center lock-scroll :show-close="false">
        <span>
          Are you sure to exit without saving? <br> Some of your changes might get lost.
        </span>
        <template #footer>
          <span class="dialog-footer">
            <el-button text bg @click="exitDialogVisible = false">Cancel</el-button>
            <el-button color="#FF0000" @click="exitWithoutSaving()">
              Exit
            </el-button>
          </span>
        </template>
      </el-dialog>
      <!-- Change name dialog -->
      <el-dialog v-model="renameNodeDialogVisible" width="25%" title="Rename Node" :show-close="false">
        <el-input v-model="renameNodeDialogName" placeholder="Please input" />
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="renameNodeDialogVisible = false">Cancel</el-button>
            <el-button type="primary" @click="renameNodeFromDialog()">
              Confirm
            </el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script lang="ts">
import { ElMessage } from "element-plus";
import * as vNG from "v-network-graph";
import type { Edges, Layouts, Node } from "v-network-graph";
import { Nodes } from "v-network-graph";
import type { AnyVariables, UseQueryState } from "@urql/vue";
import {
  useCreateEdgeMutation,
  useCreateNodeMutation,
  useDeleteEdgeMutation,
  useDeleteNodeMutation,
  useGetGraphQuery,
  useUpdateNodeMutation
} from "../graphql/graphql";

import { transformEdges, transformLayout, transformNodes } from "../tools/typeTransformers";
import { GraphSettings } from "../assets/js/graphSettings";
import type { GetGraphQuery, Graph, ScriptCell } from "@/graphql/graphql";
import { createError } from "#app";

export default {
  name: "GraphComponent",

  props: {
    uuid: {
      type: String,
      required: true
    }
  },

  data() {
    return {
      fetchedOnce: false,
      fetching: true,
      result: {},
      graphData: {} as Graph,
      error: {},

      // graph
      nodes: {} as Node,
      edges: {} as Edges,
      layouts: {} as Layouts,
      selectedNodes: [] as String[],
      selectedEdges: [] as String[],
      nextNodeIndex: 0,
      nextEdgeIndex: 0,
      configs: GraphSettings.standard,
      eventHandlers: {},
      stateSaved: true,

      // settings
      defaultNodeName: "new scene" as string,

      // interface
      menuLevel1: "edit",

      // dialogs
      exitDialogVisible: false as boolean,
      renameNodeDialogVisible: false,
      renameNodeDialogName: "",

      // node data
      showNodeData: false,
      currentNodeName: "",
      currentNodeUUID: "",

      selectedNodeScriptCells: [] as ScriptCell[],

      // debug
      showGraphData: false

      // mutations
      // createNodeMutation: () => {}
    };
  },

  computed: {
    hideConnectionButton() {
      if (this.selectedNodes.length !== 2)
        return true;
      else
        return false;
    },
    hideRemoveButton() {
      if ((this.selectedNodes.length === 0 && this.selectedEdges.length === 0) || (this.selectedNodes.length === 0 && this.selectedEdges.length === 0))
        return true;
      else if ((this.selectedNodes.length > 1 || this.selectedEdges.length > 1))
        return true;
      else
        return false;
    }
  },

  mounted() {
    this.configs.node.selectable = true;
    // event listeners

    this.eventHandlers = {
      "node:dblclick": ({ node }: Node) => {
        this.doubleClickedNode(node);
      },
      "node:dragend": ({ node }: Node) => {
        this.stateSaved = false;
        this.nodeDraggedEnd(node);
      }
    };

    this.addEmitListeners();

    // mutations
    // create node
    const { executeMutation: createNodeMutation } = useCreateNodeMutation();
    this.createNodeMutation = createNodeMutation;
    // TODO: Make simpler and use setup
    // reference: https://codesandbox.io/s/urql-hooks-typescript-example-yk3xw?file=/movies.tsx

    // update node
    const { executeMutation: updateNodeMutation } = useUpdateNodeMutation();
    this.updateNodeMutation = updateNodeMutation;

    // remove node
    const { executeMutation: removeNodeMutation } = useDeleteNodeMutation();
    this.removeNodeMutation = removeNodeMutation;

    // create edge
    const { executeMutation: createEdgeMutation } = useCreateEdgeMutation();
    this.createEdgeMutation = createEdgeMutation;

    // remove edge
    const { executeMutation: removeEdgeMutation } = useDeleteEdgeMutation();
    this.removeEdgeMutation = removeEdgeMutation;

    this.loadData();
  },

  methods: {
    ////////////////////
    // Emits
    ////////////////////

    addEmitListeners() {
      // https://github.com/nuxt/framework/discussions/2288
      this.$bus.$on("openNodeNameEdit", () => {
        this.openNodeNameEdit();
      });

      this.$bus.$on("closeNodeData", () => {
        this.closeNodeData();
      });
    },

    ////////////////////
    // interface
    ////////////////////
    exitEditing() {
      if (!this.stateSaved) {
        this.exitDialogVisible = true;
      }
      else {
        this.$router.push({
          path: "/graphs"
        });
      }
    },

    exitWithoutSaving() {
      this.$router.push({
        path: "/graphs"
      });
    },

    doubleClickedNode(node: string) {
      this.setupNodeDataWindow(node);
      this.showNodeData = true;
      console.log(this.nodes[node]);
    },

    setupNodeDataWindow(node: string) {
      this.currentNodeName = this.nodes[node].name;
      this.currentNodeUUID = node;

      const cells = this.nodes[node].scriptCells;
      this.selectedNodeScriptCells = cells;
    },

    nodeDraggedEnd(node: string) {
      // const uuid = Object.entries(node);
    },

    saveState() {
      // update positions
      for (const uuid in this.nodes) {
        // get positions
        const n = this.nodes[uuid];
        this.updateNode(uuid, n.name, n.color, this.layouts.nodes[uuid].x, this.layouts.nodes[uuid].y);
      }
      // TODO: make it async with callbacks
      this.stateSaved = true;
    },

    // node data
    closeNodeData() {
      this.showNodeData = false;
      this.selectedNodeScriptCells = [];
    },

    openNodeNameEdit() {
      this.renameNodeDialogName = this.currentNodeName;
      this.renameNodeDialogVisible = true;
    },

    renameNodeFromDialog() {
      if (this.renameNodeDialogName === "") {
        ElMessage({
          message: "Node name can't be empty",
          type: "error",
          customClass: "messages-editor"
        });
        return;
      }

      const uuid = this.currentNodeUUID;
      const n = this.nodes[uuid];
      this.currentNodeName = this.renameNodeDialogName;
      this.updateNode(uuid, this.renameNodeDialogName, n.color, this.layouts.nodes[uuid].x, this.layouts.nodes[uuid].y);
      this.renameNodeDialogVisible = false;
    },

    ////////////////////
    // graph
    ////////////////////
    async loadData() {
      const result = await useGetGraphQuery({
        variables: { uuid: this.uuid },
        requestPolicy: "network-only"
      });

      if (!result.data.value?.graph) {
        throw createError({
          statusCode: 404,
          statusMessage: "Page Not Found"
        });
      }
      this.result = result;
      // this.result = result;
      // console.log(result);
      this.graphData = result.data.value?.graph;
      this.error = result.error;
      this.fetching = result.fetching.value;

      // console.log(JSON.stringify(this.data));
      this.transformLoadedData();
      this.fetchedOnce = true;
      console.log("loaded graph");
    },

    transformLoadedData() {
      // set data
      this.transformData();
      this.nextNodeIndex = Object.keys(this.nodes).length + 1;
      this.nextEdgeIndex = Object.keys(this.edges).length + 1;
    },

    refresh() {
      // check if result is not undefined
      if (!this.result)
        return;

      (this.result as UseQueryState<GetGraphQuery, AnyVariables>).executeQuery().then(() => {
        console.log("finished refresh");
        this.transformData();
        this.selectedNodes = [];
        this.selectedEdges = [];
      });
    },

    transformData() {
      this.nodes = transformNodes(this.graphData.nodes);
      this.edges = transformEdges(this.graphData.edges);
      this.layouts = transformLayout(this.graphData.nodes);
    },

    addNode() {
      const variables = {
        graphUuid: this.uuid,
        name: this.defaultNodeName,
        color: "standard",
        positionX: 0,
        positionY: 0
      };
      this.createNodeMutation(variables).then(() => {
        this.refresh();
        console.log("Added node");
      });
    },

    addEdge() {
      if (this.selectedNodes.length !== 2) {
        ElMessage({
          message: "requires exactly 2 scenes selected.",
          type: "error",
          customClass: "messages-editor"
        });
        return;
      }
      const [source, target] = this.selectedNodes;

      const variables = {
        nodeInUuid: source,
        nodeOutUuid: target
      };

      this.createEdgeMutation(variables).then(() => {
        this.refresh();
        console.log("Added edge");
      });
    },

    updateNode(uuid: string, name: string, color: string, positionX: number, positionY: number) {
      const variables = {
        nodeUuid: uuid,
        name,
        color,
        positionX,
        positionY
      };
      this.updateNodeMutation(variables).then(() => {
        this.refresh();
        console.log("Updated node");
      });
    },

    removeAny() {
      // check if only one type is selected
      // right now we only allow one element deletion
      // needs to check if the async call is not buggy if looping through
      if ((this.selectedNodes.length === 1 && this.selectedEdges.length === 0)) {
        this.removeNode();
      }
      else if ((this.selectedNodes.length === 0 && this.selectedEdges.length === 1)) {
        this.removeEdge();
      }
      else {
        ElMessage({
          message: "Select max one scene or one connection.",
          type: "error",
          customClass: "messages-editor"
        });
      }
    },

    removeNode() {
      for (const nodeId of this.selectedNodes) {
        const variables = {
          nodeUuid: nodeId
        };

        this.removeNodeMutation(variables).then(() => {
          this.refresh();
          console.log("Removed node");
        });
      }
    },

    removeEdge() {
      for (const edgeId of this.selectedEdges) {
        const variables = {
          edgeUuid: edgeId
        };

        this.removeEdgeMutation(variables).then(() => {
          this.refresh();
          console.log("Removed edge");
        });
      }
    }
  }
};
</script>
