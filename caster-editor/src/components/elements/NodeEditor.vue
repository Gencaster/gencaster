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
  </div>
</template>

<script lang="ts">
// @ts-expect-error: Auto Imported by nuxt
import type { NodeCell } from "~/assets/js/interfaces";
// TODO: Fix typescript import to be linked in editor as well

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
    openNodeNameEdit() { },
    closeNodeData() { }
  }
};
</script>

<style lang="scss">
.node-editor-outer {
  height: inherit;
  widows: inherit;
  padding: 5px 15px 15px 15px;
  background-color: $mainWhite;
  border: 1px solid $black;
  overflow-y: scroll;

  .title {
    display: flex;
    height: $menuHeight;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;

    .left {
      button {
        color: $grey-dark;

        &:hover {
          font-style: italic;
          background-color: transparent;
        }
      }
    }

    .right {
      transform: translateX(8px);
      text-decoration: underline;
    }

    .left,
    .right {
      display: flex;
      justify-content: center;
      align-items: center;

      p {
        margin: 0;
      }
    }
  }

  .node-menu-bar {
    display: flex;
    height: $menuHeight;
    background-color: $grey-light;
    border-radius: 4px;
    margin-bottom: 12px;

    .el-icon svg {
      transform: scale(1.5);
    }
  }

  .blocks {
    display: block;
    position: relative;

    .cell {
      position: relative;
      margin-bottom: $spacingM;
      border-radius: 4px;
      background-color: $grey-light;
      padding: 20px 20px 15px 20px;
      border: 1px solid #CDCDCD;

      .cell-type {
        position: absolute;
        top: 4px;
        right: 8px;
        color: $grey-dark;
        font-style: italic;
      }

      .drag-button {
        cursor: ns-resize;
        width: 30px;
        height: 25px;
        position: absolute;
        bottom: 12px;
        right: 8px;

        .bar {
          width: 30px;
          height: 1px;
          background-color: $grey-dark;
          margin-top: 8px;
        }

      }

      .cell-editor {
        width: calc(100% - 40px);
      }
    }
  }

}
</style>
