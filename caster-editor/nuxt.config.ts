const metaTitle = "Gencaster - Editor";

export default defineNuxtConfig({

  app: {
    // pageTransition: { name: 'page', mode: 'out-in' },
    head: {
      title: metaTitle
    }
  },

  //   theme: {
  //     dark: true,
  //     colors: {
  //       primary: '#ff0000',
  //     },
  //   },
  // imports: {
  //   autoImport: false
  // },
  modules: ["nuxt-vitest"],
  telemetry: false,
  typescript: {
    shim: false
  },
  ssr: false,
  css: ["assets/scss/main.scss", "v-network-graph/lib/style.css"],
  components: false,
  srcDir: "src/",
  runtimeConfig: {
    public: {
      BACKEND_GRAPHQL_URL: process.env.BACKEND_GRAPHQL_URL || "http://127.0.0.1:8081/graphql"
    }
  }
});
