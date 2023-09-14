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
import {
  reactive,
  ref,
  onMounted,
  onDeactivated,
  type Ref,
  computed,
} from "vue";
import type { GraphSubscription, Graph } from "@/graphql";
import "@toast-ui/editor/dist/toastui-editor.css"; // Editor's Style
import type { EditorOptions, Editor as EditorType } from "@toast-ui/editor";
import Editor from "@toast-ui/editor";
import Wysiwyg from "@/components/Wysiwyg.vue";
import { useInterfaceStore, Tab } from "@/stores/InterfaceStore";

import { storeToRefs } from "pinia";
const { tab } = storeToRefs(useInterfaceStore());

// props
// const props = defineProps<{
//   graph: GraphSubscription["graph"];
// }>();

const props = defineProps<{
  graph: Graph;
  showDebug?: boolean;
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

const metaForm = reactive({
  projectName: "",
  displayName: "",
  slug: "",
  streamAssignment: "",
  introText: "",
  aboutText: "",
  endText: "",
});

// cloning needs plugin, so just being redundant for now
const metaFormOriginal = reactive({
  projectName: "",
  displayName: "",
  slug: "",
  streamAssignment: "",
  introText: "",
  aboutText: "",
  endText: "",
});

const saveButtonActive = computed(() => {
  if (JSON.stringify(metaForm) !== JSON.stringify(metaFormOriginal)) {
    return true;
  } else {
    return false;
  }
});

const onSubmit = () => {
  console.log("Submitted");
  console.log(metaForm);
};

const onCancel = () => {
  // tab.value = Tab.Edit;
  console.log(JSON.stringify(metaForm));
};

const populateData = () => {
  // form
  metaForm.projectName = props.graph.name;
  metaForm.displayName = props.graph.displayName;
  metaForm.slug = props.graph.slugName;
  metaForm.streamAssignment = "one_graph_one_stream";
  metaForm.introText = props.graph.startText;
  metaForm.aboutText = props.graph.aboutText;
  metaForm.endText = props.graph.endText;

  // original data
  metaFormOriginal.projectName = props.graph.name;
  metaFormOriginal.displayName = props.graph.displayName;
  metaFormOriginal.slug = props.graph.slugName;
  metaFormOriginal.streamAssignment = "one_graph_one_stream";
  metaFormOriginal.introText = props.graph.startText;
  metaFormOriginal.aboutText = props.graph.aboutText;
  metaFormOriginal.endText = props.graph.endText;
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
          <Wysiwyg :text="metaForm.introText" />
        </ElFormItem>
      </ElCol>

      <ElCol :span="24">
        <ElFormItem label="About Text">
          <Wysiwyg :text="metaForm.aboutText" />
        </ElFormItem>
      </ElCol>
      <ElCol :span="24">
        <ElFormItem label="End Text">
          <Wysiwyg :text="metaForm.endText" />
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
          Cancel
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
  // background-color: red;

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
