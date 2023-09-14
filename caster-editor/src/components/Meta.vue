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
  ElSwitch,
  ElMessage,
} from "element-plus";
import { ref, type Ref, watch, computed } from "vue";
import "@toast-ui/editor/dist/toastui-editor.css"; // Editor's Style
import Wysiwyg from "@/components/Wysiwyg.vue";
import {
  useGetGraphQuery,
  useUpdateGraphMutation,
  StreamAssignmentPolicy,
  type UpdateGraphInput,
} from "@/graphql";

const props = defineProps<{
  graphUuid: string;
}>();

const { executeQuery } = useGetGraphQuery({
  variables: { graphUuid: props.graphUuid },
});
const updateGraphMutation = useUpdateGraphMutation();
const { data, error, fetching } = executeQuery();

watch(error, (errorMsg) => {
  ElMessage.error(
    `Could not obtain meta data of graph ${props.graphUuid}: ${errorMsg?.message}`,
  );
});

watch(data, (newData) => {
  formData.value = newData?.graph ?? {};
  saveOriginalData();
});

const originalData: Ref<UpdateGraphInput> = ref({});

const saveOriginalData = () => {
  originalData.value = { ...formData.value };
};

const compareData = computed(() => {
  return JSON.stringify(formData.value) === JSON.stringify(originalData.value);
});

const formData: Ref<UpdateGraphInput> = ref({});

const mutationRuns: Ref<boolean> = ref<boolean>(false);

const onSubmit = async () => {
  mutationRuns.value = true;
  // formData also contains data that does not belong to the input such as UUID or slugName
  // while ts/js does not have a problem with that, graphql has and throws an error, therefore we need
  // to provide/copy an explicit mapping here
  // see https://stackoverflow.com/questions/75299141/how-to-type-safely-remove-a-property-from-a-typescript-type
  // and https://stackoverflow.com/questions/43909566/get-keys-of-a-typescript-interface-as-array-of-strings
  const {
    name,
    displayName,
    startText,
    aboutText,
    endText,
    publicVisible,
    streamAssignmentPolicy,
    templateName,
  } = formData.value;
  const { error } = await updateGraphMutation.executeMutation({
    graphUuid: props.graphUuid,
    graphUpdate: {
      name,
      displayName,
      startText,
      aboutText,
      endText,
      publicVisible,
      streamAssignmentPolicy,
      templateName,
    },
  });
  if (error) {
    ElMessage.error(`Failed to update the meta-data: ${error.message}`);
  } else {
  }
  mutationRuns.value = false;
  executeQuery();
};
</script>

<template>
  <div
    v-loading="fetching || mutationRuns"
    class="meta-wrapper"
  >
    <ElForm
      :model="formData"
      label-width="150px"
      label-position="top"
      inline
    >
      <ElCol :span="12">
        <ElFormItem label="Project name">
          <ElInput
            v-model="formData.name"
            placeholder="Project Name"
          />
        </ElFormItem>
      </ElCol>

      <ElCol :span="12">
        <ElFormItem label="Display name">
          <ElInput
            v-model="formData.displayName"
            placeholder="Display Name"
          />
        </ElFormItem>
      </ElCol>

      <ElCol :span="12">
        <ElFormItem label="Slug">
          <ElInput
            :model-value="data?.graph.slugName"
            placeholder="Slug"
            readonly
            @focus="
              () => {
                ElMessage.info(
                  'Please use backend admin interface to edit the slug value'
                );
              }
            "
          />
        </ElFormItem>
      </ElCol>

      <ElCol :span="12">
        <ElFormItem label="Stream assignment">
          <ElSelect
            v-if="formData.streamAssignmentPolicy != undefined"
            v-model="formData.streamAssignmentPolicy"
            :placeholder="StreamAssignmentPolicy.OneUserOneStream"
          >
            <ElOption
              v-for="(policyValue, policyName) in StreamAssignmentPolicy"
              :key="policyValue"
              :label="policyName"
              :value="policyValue"
            />
          </ElSelect>
        </ElFormItem>
      </ElCol>

      <ElCol :span="12">
        <ElFormItem label="Intro Text">
          <ElInput
            v-model="formData.startText"
            placeholder="Start Text"
            show-word-limit
            type="text"
            maxlength="60"
          />
        </ElFormItem>
      </ElCol>

      <ElCol :span="12">
        <ElFormItem
          label="Listed publicly"
          prop="publicVisible"
        >
          <ElSwitch
            v-if="formData.publicVisible != undefined"
            v-model="formData.publicVisible"
          />
        </ElFormItem>
      </ElCol>

      <ElCol :span="24">
        <ElFormItem label="About Text">
          <Wysiwyg
            v-if="formData.aboutText != undefined"
            :text="formData.aboutText"
            @update-text="
              (text) => {
                formData.aboutText = text;
              }
            "
          />
        </ElFormItem>
      </ElCol>
      <ElCol :span="24">
        <ElFormItem label="End Text">
          <Wysiwyg
            v-if="formData.endText != undefined"
            :text="formData.endText"
            @update-text="(text: any) => {formData.endText = text}"
          />
        </ElFormItem>
      </ElCol>

      <ElFormItem class="save-buttons">
        <ElButton
          type="primary"
          :disabled="compareData"
          @click="onSubmit"
        >
          Save
        </ElButton>
        <ElButton
          :disabled="compareData"
          @click="
            () => {
              executeQuery();
            }
          "
        >
          Discard changes
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
