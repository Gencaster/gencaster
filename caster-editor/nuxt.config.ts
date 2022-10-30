// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
  title: 'Gencaster - Editor',
  //   theme: {
  //     dark: true,
  //     colors: {
  //       primary: '#ff0000',
  //     },
  //   },
  css: ['~/assets/scss/main.scss', 'v-network-graph/lib/style.css'],
  components: true,

  port: 3001,
});
