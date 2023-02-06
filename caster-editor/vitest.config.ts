import { defineVitestConfig } from "nuxt-vitest/config";
import { alias } from "./alias";

export default defineVitestConfig({
  root: ".",
  esbuild: {
    tsconfigRaw: "{}"
  },
  resolve: {
    alias
  },
  test: {
    globals: true
  }
});
