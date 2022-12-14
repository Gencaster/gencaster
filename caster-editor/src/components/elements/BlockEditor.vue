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
        <div class="cell" :class="{ 'no-padding': noPadding(cell.cellType) }">
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
      <button class="unstyled" @click="toggleShowJSONData()">
        JSON
      </button>
    </div>
    <div v-if="showJSONData" class="json">
      <Codemirror
        v-model="JSONViewerData" placeholder="Code goes here..." :autofocus="false" :indent-with-tab="true"
        :tab-size="2" :extensions="extensions" :disabled="true"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { Codemirror } from "vue-codemirror";
import { Plus, Scissor, VideoPause, VideoPlay } from "@element-plus/icons-vue";
import { json } from "@codemirror/lang-json";
import { computed } from "vue";
import type { ScriptCell } from "@/graphql/graphql";
import { CellType } from "@/graphql/graphql";

const props = defineProps({
  dev: Boolean,
  blocksData: Array<ScriptCell>,
  currentNodeName: String
});

const { $bus } = useNuxtApp();

// Variables
const extensions = [json()];

// interface
const showJSONData = ref(false);

// Computed
const JSONViewerData = computed(() => {
  return JSON.stringify({ data: props.blocksData }, null, 2);
});

const noPadding = (blockCellType: CellType) => {
  if (blockCellType === CellType.Markdown || blockCellType === CellType.Comment)
    return true;
  else
    return false;
};

// Methods
const openNodeNameEdit = () => {
  $bus.$emit("openNodeNameEdit");
};

const closeNodeData = () => {
  $bus.$emit("closeNodeData");
};

const toggleShowJSONData = () => {
  showJSONData.value = !showJSONData.value;
};
</script>
