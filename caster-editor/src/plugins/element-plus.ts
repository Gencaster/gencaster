import { defineNuxtPlugin } from '#app';
import * as ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';

export default defineNuxtPlugin(
  (nuxtApp: { vueApp: { use: (arg0: typeof ElementPlus) => void } }) => {
    nuxtApp.vueApp.use(ElementPlus);
  }
);
