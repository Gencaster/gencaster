import vuedraggable from "vuedraggable";

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.component("draggable", vuedraggable);
});
