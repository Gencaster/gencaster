import mitt from "mitt";
import { defineNuxtPlugin } from "#app";
const emitter = mitt();

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.provide("bus", {
    $on: emitter.on,
    $emit: emitter.emit
  });
});
