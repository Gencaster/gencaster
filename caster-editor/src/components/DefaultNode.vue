<script lang="ts" setup>
import { Handle, Position } from "@vue-flow/core";
import { computed } from "vue";

interface DataInput {
  name: {
    type: String;
    required: true;
  };
  uuid: {
    type: String;
    required: true;
  };
  scriptCells: {
    type: Array;
    required: true;
  };
}

const props = defineProps({
  //TODO: needs to be typed correctly
  data: {
    type: Object as PropType<DataInput>,
    required: true,
  },
});

const emit = defineEmits(["dblclick"]);

function onDblClick() {
  emit("dblclick", uuid);
}

// function onGradient() {
//   emit('gradient');
// }

// const presets = {
//   sumi: '#1C1C1C',
//   gofun: '#FFFFFB',
//   byakuroku: '#A8D8B9',
//   mizu: '#81C7D4',
//   asagi: '#33A6B8',
//   ukon: '#EFBB24',
//   mushikuri: '#D9CD90',
//   hiwa: '#BEC23F',
//   ichigo: '#B5495B',
//   kurenai: '#CB1B45',
//   syojyohi: '#E83015',
//   konjyo: '#113285',
//   fuji: '#8B81C3',
//   ayame: '#6F3381',
//   torinoko: '#DAC9A6',
//   kurotsurubami: '#0B1013',
//   ohni: '#F05E1C',
//   kokikuchinashi: '#FB9966',
//   beniukon: '#E98B2A',
//   sakura: '#FEDFE1',
//   toki: '#EEA9A9',
// };

// const colors = Object.keys(presets).map((color) => {
//   return {
//     name: color,
//     value: presets[color],
//   };
// });

// const sourceHandleStyleA = computed(() => ({ backgroundColor: props.data.color, filter: 'invert(100%)', top: '10px' }));

// const sourceHandleStyleB = computed(() => ({
//   backgroundColor: props.data.color,
//   filter: 'invert(100%)',
//   bottom: '10px',
//   top: 'auto',
// }));

const sourceHandleStyleA = computed(() => ({
  backgroundColor: "red",
  top: "10px",
  width: "10px",
  height: "10px",
}));

// const sourceHandleStyleB = computed(() => ({
//   backgroundColor: 'red', top: '10px', width: '10px', height: '10px',
// }));
</script>

<template>
  <div class="node default-node">
    <p>{{ data.name }}</p>
    <p>{{ data.uuid }}</p>

    <button @click="onDblClick">
      dblclick
    </button>

    <Handle
      id="a"
      type="source"
      :position="Position.Bottom"
      :style="sourceHandleStyleA"
    />

    <!-- <Handle
      id="b"
      type="source"
      :position="Position.Right"
      :style="sourceHandleStyleB"
    /> -->
  </div>
</template>

<style lang="scss" scoped>
@import "@/assets/scss/variables.module.scss";

.node {
  padding: 10px;
  border-radius: 4px;
  height: auto;
  background-color: yellow;
  width: 200px;
  border: 1px solid black;
}
</style>
