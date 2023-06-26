
<script setup lang="ts">
import { ref } from 'vue';
import { ElCollapse, ElCollapseItem, ElTable, ElTableColumn } from 'element-plus';
import type { Node } from '@/graphql';
export type NodeName = Pick<Node, 'name' | 'uuid'>

const props = defineProps<{
    node: NodeName
}>();

const activeNames = ref(['']);

const tableData = ref([
  {
    name: 'name',
    data: props.node.name,
  },
  {
    name: 'uuid',
    data: props.node.uuid,
  },
]);


</script>

<template>
  <div class="dev-info">
    <ElCollapse
      v-model="activeNames"
    >
      <ElCollapseItem
        title="Dev Info"
        name="1"
      >
        <ElTable
          :data="tableData"
          :fit="true"
        >
          <ElTableColumn
            prop="name"
            label="Name"
          />
          <ElTableColumn
            prop="data"
            label="Data"
          />
        </ElTable>
      </ElCollapseItem>
    </ElCollapse>
  </div>
</template>


<style lang="scss" scoped>
@import '@/assets/scss/variables.module.scss';

.dev-info {
  display: block;
  position: relative;
  padding-left: 15px;
  padding-right: 15px;
  margin-top: calc($menuHeight*4);
  margin-bottom: calc($menuHeight*1);

  :deep(.el-collapse-item__header) {
    font-size: $baseFontSize;
  }

  :deep(.cell) {
    padding: 0;
  }
}
</style>
