<template>
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
          <span>
            {{ graph.name }}
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
</template>

<script lang="ts" setup>

</script>
