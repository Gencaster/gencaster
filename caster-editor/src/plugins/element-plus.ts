import * as ElementPlus from "element-plus";
// @ts-expect-error: Auto Imported by nuxt
import { defineNuxtPlugin } from "#app";
import "element-plus/dist/index.css";

export default defineNuxtPlugin(
  (nuxtApp: { vueApp: { use: (arg0: typeof ElementPlus) => void } }) => {
    nuxtApp.vueApp.use(ElementPlus);
  }
);
