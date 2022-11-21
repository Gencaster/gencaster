// This is a nuxt specific setup to give element-plus components a unique reference in the renderlogic.
// It was taken from their examples
import { ID_INJECTION_KEY } from "element-plus";

// @ts-expect-error: Auto Imported by nuxt
import type { NuxtApp } from "#app";
// @ts-expect-error: Auto Imported by nuxt
import { defineNuxtPlugin } from "#app";

export default defineNuxtPlugin((nuxtApp: NuxtApp) => {
  // const elementPlusPlugin = {};
  nuxtApp.vueApp.provide(ID_INJECTION_KEY, {
    prefix: Math.floor(Math.random() * 10000),
    current: 0
  });
});
