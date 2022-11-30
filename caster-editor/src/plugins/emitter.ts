import mitt from "mitt";
// @ts-expect-error: Auto Imported by nuxt
import { defineNuxtPlugin } from "#app";
const emitter = mitt();

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.provide("bus", {
    $on: emitter.on,
    $emit: emitter.emit
  });
});
