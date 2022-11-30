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
  </div>
</template>

<script lang="ts">
export default {
  name: "NodeEditor",

  props: {
    dev: {
      type: Boolean,
      required: false,
      default: () => false
    },
    blockData: {
      type: Array,
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
    openNodeNameEdit() {},
    closeNodeData() {}
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

}
</style>
