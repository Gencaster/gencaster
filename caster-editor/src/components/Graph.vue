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
              {{ data.graph.name }}
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
    <div v-else>
      <p v-if="showGraphData">
        {{ nodes }}
        <br>
        {{ layouts }}
        <br>
        {{ data.graph }}
        <!-- {{ data.graph }} -->
      </p>
      <v-network-graph
        v-model:selected-nodes="selectedNodes" v-model:selected-edges="selectedEdges" class="graph"
        :nodes="nodes" :edges="edges" :configs="configs" :layouts="layouts" :event-handlers="eventHandlers"
      />

      <div v-if="showNodeData" class="node-data">
        <ElementsBlockEditor :blocks-data="selectedNodeScriptCells" />
        <!-- <div class="title">
          <div class="left">
            <p>{{ currentNodeName }}</p>
            <button class="unstyled" @click="openNodeNameEdit()">
              edit
            </button>
          </div>
          <div class="right">
            <button class="unstyled" @click="closeNodeData()">
              Close
            </button>
          </div>
        </div>
        <div class="node-menu-bar">
          <el-button text bg :icon="Plus" />
          <el-button text bg :icon="Scissor" />
          <el-button text bg :icon="VideoPlay" />
          <el-button text bg :icon="VideoPause" />
        </div>
        <div class="blocks">
          {{ selectedNodeScriptCells }}
        </div>
        <div class="footer">
          <button class="unstyled" @click="showNodeDataJSON()">
            JSON
          </button>
        </div> -->
      </div>

      <div v-if="!showNodeData" class="stats">
        <p>
          Nodes: {{ data.graph.nodes.length }} &nbsp;
          Edges: {{ data.graph.edges.length }}
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
import { Edges, Nodes } from "v-network-graph";
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

export default {
  name: "GraphComponent",

  props: {
    uuid: {
      type: String,
      required: true
    }
  },

  data() {
    interface Cell {
      uuid: string
      cellType: string
      cellCode: string
    }

    return {
      fetching: true,
      result: null,
      data: {
        graph: {
          name: "",
          edges: [],
          nodes: []
        }
      },
      error: null,

      // graph
      nodes: {},
      edges: {},
      layouts: {},
      selectedNodes: new Array<string>(),
      selectedEdges: new Array<string>(),
      nextNodeIndex: 0,
      nextEdgeIndex: 0,
      configs: vNG.getFullConfigs(),
      eventHandlers: undefined,
      stateSaved: true,

      // settings
      defaultNodeName: "new scene",

      // interface
      menuLevel1: "edit",

      // dialogs
      exitDialogVisible: false,
      renameNodeDialogVisible: false,
      renameNodeDialogName: "",

      // node data
      showNodeData: false,
      currentNodeName: "",
      currentNodeUUID: "",
      // TODO Import the interface ontop
      selectedNodeScriptCells: [],
      editors: [],

      // debug
      showGraphData: false
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

  // onBeforeUnmount() {
  //   this.destroyEditors();
  // },

  mounted() {
    this.configs.node.selectable = true;
    // event listeners

    this.eventHandlers = {
      "node:dblclick": ({ node }) => {
        this.doubleClickedNode(node);
      },
      "node:dragend": (node) => {
        this.stateSaved = false;
        this.nodeDraggedEnd(node);
      }
    };

    // mutations
    // create node
    const { executeMutation: createNodeMutation } = useCreateNodeMutation();
    this.createNodeMutation = createNodeMutation;

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

    this.configs = GraphSettings.standard;

    this.loadData();
  },

  methods: {
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

    doubleClickedNode(node) {
      this.setupNodeDataWindow(node);
      this.showNodeData = true;
      console.log(this.nodes[node]);
    },

    destroyEditors() {
      this.editors.forEach((editor) => {
        editor.destroy();
      });
    },

    setupNodeDataWindow(node) {
      this.currentNodeName = this.nodes[node].name;
      this.currentNodeUUID = node;
      // empty editors
      this.destroyEditors();

      const cells = this.nodes[node].scriptCells;
      // cells.forEach((cell) => {
      //   const editor = new Editor({
      //     content: cell.cellCode,
      //     extensions: [
      //       StarterKit
      //     ]
      //   });

      //   this.editors.push(editor);
      // });

      this.selectedNodeScriptCells = cells;
    },

    nodeDraggedEnd(node) {
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

    showNodeDataJSON() {
      // TODO: Write the json display
      console.log("show node data");
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

      this.result = result;
      this.data = result.data;
      this.error = result.error;
      this.fetching = result.fetching;

      // console.log(JSON.stringify(this.data));
      console.log("loaded graph");
      this.loadedData();
    },

    loadedData() {
      // set data
      this.transformData();
      this.nextNodeIndex = Object.keys(this.nodes).length + 1;
      this.nextEdgeIndex = Object.keys(this.edges).length + 1;
    },

    refresh() {
      this.result.executeQuery().then(() => {
        console.log("finished refresh");
        this.transformData();
        this.selectedNodes = [];
        this.selectedEdges = [];
      });
    },

    transformData() {
      this.nodes = transformNodes(this.data.graph.nodes);
      this.edges = transformEdges(this.data.graph.edges);
      this.layouts = transformLayout(this.data.graph.nodes);
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
