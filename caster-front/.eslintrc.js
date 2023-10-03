/* eslint-env node */
require("@rushstack/eslint-patch/modern-module-resolution");

module.exports = {
  extends: [
    "plugin:vue/vue3-recommended",
    "@vue/eslint-config-typescript",
  ],
  rules: {
    "no-console": "off",
    "no-alert": "off",
    "semi": ['error', 'always'],
    "vue/component-tags-order": ["error", {
      "order": [ "script", "template", "style" ],
    }],
    "vue/multi-word-component-names": "off",
    "vue/no-v-model-argument": "off",
    "comma-dangle": ["error", {
      "arrays": "always-multiline",
      "objects": "always-multiline",
      "imports": "always-multiline",
      "exports": "always-multiline",
      "functions": "always-multiline",
  }],
  },
};
