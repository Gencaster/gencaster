import svgLoader from "vite-svg-loader";

export default defineNuxtConfig({
  //   theme: {
  //     dark: true,
  //     colors: {
  //       primary: '#ff0000',
  //     },
  //   },
  // imports: {
  //   autoImport: false
  // },
  modules: ["@pinia/nuxt"],
  typescript: {
    shim: false
  },
  ssr: false,
  css: ["assets/scss/main.scss", "v-network-graph/lib/style.css"],
  components: true,
  srcDir: "src/",
  runtimeConfig: {
    public: {
      BACKEND_GRAPHQL_URL: process.env.BACKEND_GRAPHQL_URL || "http://127.0.0.1:8081/graphql"
    }
  },
  vite: {
    plugins: [
      svgLoader({
        /* ... */
      })
    ]
  }
});
