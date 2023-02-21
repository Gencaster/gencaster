<script lang="ts" setup>
import { storeToRefs } from "pinia";
import { useStreamPointStore } from "@/stores/StreamPoints";

const { graphs, selectedGraphUuid } = storeToRefs(useStreamPointStore());
</script>

<template>
  <div>
    <ul>
      <li v-for="graph in graphs?.graphs" :key="graph.uuid">
        <span @click="() => { selectedGraphUuid = graph.uuid }">
          Graph {{ graph.name }}
        </span>
      </li>
    </ul>
  </div>
</template>
