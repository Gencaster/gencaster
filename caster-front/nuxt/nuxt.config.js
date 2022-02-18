export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'drifter - beta',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: ['~/assets/scss/global.scss'],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [{ src: '~/plugins/mapbox', mode: 'client' }],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/eslint
    '@nuxtjs/eslint-module',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    // https://go.nuxtjs.dev/pwa
    '@nuxtjs/pwa',
    '@nuxtjs/style-resources',
  ],

  styleResources: {
    scss: ['~/assets/scss/variables.scss'],
  },

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    baseURL: '/',
  },

  // PWA module configuration: https://go.nuxtjs.dev/pwa
  pwa: {
    manifest: {
      lang: 'en',
    },
  },

  // https://nuxtjs.org/blog/moving-from-nuxtjs-dotenv-to-runtime-config#using-your-config-values
  publicRuntimeConfig: {
    // SOCKETURL: process.env.SOCKETURL || 'http://localhost:1312/',
    SOCKETURL:
      process.env.NODE_ENV === 'production'
        ? 'https://backend.gencast.augmented.audio/'
        : 'http://localhost:1337/',
  }, // public to the frontend

  privateRuntimeConfig: {}, // private to the frontend

  // [ ] create a custom .env to fill out those vars
  server: {
    port: process.env.NUXTPORT || 3000, // default: 3000
    host: process.env.NUXTHOST || '127.0.0.1', // default: localhost 0.0.0.0 for sharing // 127.0.0.1 for online
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {},
}
