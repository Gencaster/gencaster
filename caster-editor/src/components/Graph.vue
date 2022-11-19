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
            <button class="unstyled">
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
        {{ data.graph }}
      </p>
      <v-network-graph
        v-model:selected-nodes="selectedNodes" v-model:selected-edges="selectedEdges" class="graph"
        :nodes="nodes" :edges="edges" :configs="configs"
      />

      <div class="stats">
        <p>
          Nodes: {{ data.graph.nodes.length }} &nbsp;
          Edges: {{ data.graph.edges.length }}
        </p>
      </div>

      <!-- Dialogs -->
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
  useGetGraphQuery
} from "../graphql/graphql";

import { transformEdges, transformNodes } from "../tools/typeTransformers";
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
      selectedNodes: new Array<string>(),
      selectedEdges: new Array<string>(),
      nextNodeIndex: 0,
      nextEdgeIndex: 0,
      transformEdges,
      transformNodes,
      configs: vNG.getFullConfigs(),
      stateSaved: true,

      // settings
      defaultNodeName: "new scene",

      // interface
      menuLevel1: "edit",
      exitDialogVisible: false,

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

  mounted() {
    this.configs.node.selectable = true;

    // add node
    const { executeMutation: addNodeMutation } = useCreateNodeMutation();
    this.addNodeMutation = addNodeMutation;

    // remove node
    const { executeMutation: removeNodeMutation } = useDeleteNodeMutation();
    this.removeNodeMutation = removeNodeMutation;

    // add edge
    const { executeMutation: addEdgeMutation } = useCreateEdgeMutation();
    this.addEdgeMutation = addEdgeMutation;

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
      this.nodes = transformNodes(this.data.graph.nodes);
      this.edges = transformEdges(this.data.graph.edges);

      this.nextNodeIndex = Object.keys(this.nodes).length + 1;
      this.nextEdgeIndex = Object.keys(this.edges).length + 1;
    },

    refresh() {
      this.result.executeQuery().then(() => {
        console.log("finished refresh");
        this.nodes = transformNodes(this.data.graph.nodes);
        this.edges = transformEdges(this.data.graph.edges);
        this.selectedNodes = [];
        this.selectedEdges = [];
      });
    },

    addNode() {
      const variables = {
        graphUuid: this.uuid,
        name: this.defaultNodeName,
        color: "standard",
        positionX: 0,
        positionY: 0
      };
      this.addNodeMutation(variables).then(() => {
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

      this.addEdgeMutation(variables).then(() => {
        this.refresh();
        console.log("Added edge");
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
