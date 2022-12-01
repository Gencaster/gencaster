<script setup lang="ts">
import { Plus, Scissor, VideoPause, VideoPlay } from "@element-plus/icons-vue";
</script>

<template>
  <div class="node-editor-outer">
    <div class="title">
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
      <div v-for="cell in blocksData" :key="cell.uuid">
        <!-- {{ cell.cellCode }} -->
        <div class="cell">
          <p class="cell-type">
            {{ cell.cellType }}
          </p>
          <div class="drag-button">
            <div class="bar" />
            <div class="bar" />
            <div class="bar" />
          </div>
          <ElementsBlock :cell-data="cell" class="cell-editor" />
        </div>
      </div>
    </div>
    <div class="footer">
      <button class="unstyled" @click="showNodeDataJSON()">
        JSON
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import type { NodeCell } from "@/assets/js/interfaces";

export default {
  name: "NodeEditor",

  props: {
    dev: {
      type: Boolean,
      required: false,
      default: () => false
    },
    blocksData: {
      type: Array<NodeCell>,
      required: true,
      default: () => []
    },
    currentNodeName: {
      type: String,
      required: false,
      default: () => "Placeholder"
    }
  },

  data() {
    return {};
  },

  computed: {
  },

  mounted() {
  },

  methods: {
    openNodeNameEdit() {
      this.$bus.$emit("openNodeNameEdit");
    },
    closeNodeData() {
      this.$bus.$emit("closeNodeData");
    },
    showNodeDataJSON() {
      // TODO: Write the json display
      console.log("show node data");
    }
  }
};
</script>
