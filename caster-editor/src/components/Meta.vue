<!-- eslint-disable vue/no-v-model-argument -->
<script lang="ts" setup>
import {
  ElButton,
  ElInput,
  ElSelect,
  ElOption,
  ElForm,
  ElFormItem,
  ElCol,
} from "element-plus";
import { ref, computed } from "vue";
import type { GraphSubscription } from "@/graphql";
import "@toast-ui/editor/dist/toastui-editor.css"; // Editor's Style

import Wysiwyg from "@/components/Wysiwyg.vue";
import { useInterfaceStore, Tab } from "@/stores/InterfaceStore";

import { storeToRefs } from "pinia";
const { tab } = storeToRefs(useInterfaceStore());

// props
const props = defineProps<{
  graph: GraphSubscription["graph"];
}>();

// TODO: Import from graphql
const streamAssignmentOptions = [
  {
    value: "one_graph_one_stream",
    label: "Each graph has only one stream",
  },
  {
    value: "one_user_one_stream",
    label: "Each user gets its own stream",
  },
  {
    value: "deactivate",
    label: "No stream assignment",
  },
];

const metaForm = ref({
  projectName: "",
  displayName: "",
  slug: "",
  streamAssignment: "",
  startText: "",
  aboutText: "",
  endText: "",
});

// cloning needs plugin, so just being redundant for now
const metaFormOriginal = ref({
  projectName: "",
  displayName: "",
  slug: "",
  streamAssignment: "",
  startText: "",
  aboutText: "",
  endText: "",
});

const saveButtonActive = computed(() => {
  if (
    JSON.stringify(metaForm.value) !== JSON.stringify(metaFormOriginal.value)
  ) {
    return true;
  } else {
    return false;
  }
});

const populateData = () => {
  // form
  metaForm.value.projectName = props.graph.name;
  metaForm.value.displayName = props.graph.displayName;
  metaForm.value.slug = props.graph.slugName;
  metaForm.value.streamAssignment = "one_graph_one_stream";
  metaForm.value.startText = props.graph.startText;
  metaForm.value.aboutText = props.graph.aboutText;
  metaForm.value.endText = props.graph.endText;

  // original data
  metaFormOriginal.value.projectName = props.graph.name;
  metaFormOriginal.value.displayName = props.graph.displayName;
  metaFormOriginal.value.slug = props.graph.slugName;
  metaFormOriginal.value.streamAssignment = "one_graph_one_stream";
  metaFormOriginal.value.startText = props.graph.startText;
  metaFormOriginal.value.aboutText = props.graph.aboutText;
  metaFormOriginal.value.endText = props.graph.endText;
};

// TODO: remove redundancy by abstracting
// somehow I couldn't figure out how to pass the reference to the function
// const updatedMarkdown = (text: string, reference: Ref) => {
// };

const updateAbout = (text: string) => {
  metaForm.value.aboutText = text;
};

const updateEnd = (text: string) => {
  metaForm.value.endText = text;
};

// TODO: Submit Data
const onSubmit = () => {
  console.log("Submitted");
  console.log(metaForm);
};

const onCancel = () => {
  tab.value = Tab.Edit;
};

populateData();
</script>

<template>
  <div class="meta-wrapper">
    <ElForm
      :model="metaForm"
      label-width="150px"
      label-position="top"
      inline
    >
      <ElCol :span="12">
        <ElFormItem label="Project name">
          <ElInput
            v-model="metaForm.projectName"
            placeholder="Project Name"
          />
        </ElFormItem>
      </ElCol>

      <ElCol :span="12">
        <ElFormItem label="Display name">
          <ElInput
            v-model="metaForm.displayName"
            placeholder="Display Name"
          />
        </ElFormItem>
      </ElCol>

      <ElCol :span="12">
        <ElFormItem label="Slug">
          <ElInput
            v-model="metaForm.slug"
            placeholder="Slug"
            disabled
          />
        </ElFormItem>
      </ElCol>

      <ElCol :span="12">
        <ElFormItem label="Stream assignment">
          <ElSelect
            v-model="metaForm.streamAssignment"
            placeholder="Select"
          >
            <ElOption
              v-for="item in streamAssignmentOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </ElSelect>
        </ElFormItem>
      </ElCol>

      <ElCol :span="24">
        <ElFormItem label="Intro Text">
          <ElInput
            v-model="metaForm.startText"
            placeholder="Start Text"
            show-word-limit
            type="text"
            maxlength="60"
          />
        </ElFormItem>
      </ElCol>

      <ElCol :span="24">
        <ElFormItem label="About Text">
          <Wysiwyg
            :text="metaForm.aboutText"
            @update-text="updateAbout($event)"
          />
        </ElFormItem>
      </ElCol>
      <ElCol :span="24">
        <ElFormItem label="End Text">
          <Wysiwyg
            :text="metaForm.endText"
            @update-text="updateEnd($event)"
          />
        </ElFormItem>
      </ElCol>

      <ElFormItem class="save-buttons">
        <ElButton
          type="primary"
          :disabled="!saveButtonActive"
          @click="onSubmit"
        >
          Save
        </ElButton>
        <ElButton @click="onCancel">
          Discard
        </ElButton>
      </ElFormItem>
    </ElForm>
  </div>
</template>

<style lang="scss" scoped>
@import "@/assets/scss/variables.module.scss";

.meta-wrapper {
  position: absolute;
  top: 64px;
  left: 0;
  width: 100%;
  height: calc(100vh - 64px);
  background-color: $white;
  overflow-y: scroll;
  padding: $spacingM;
  padding-top: $spacingM;

  .el-form {
    max-width: 740px;
    width: 100%;
    margin: 0 auto;
    // background-color: yellow;

    :deep(.el-select) {
      width: 100%;
    }
  }

  .save-buttons {
    position: absolute;
    top: calc(64px + #{$spacingM});
    top: #{$spacingM};
    right: $spacingM;
    margin: 0;
  }
}
</style>
