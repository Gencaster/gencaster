import { defineNuxtPlugin } from '#app'
import urql from '@urql/vue'

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.use(urql, {
    url: 'http://127.0.0.1:8081/graphql',
    requestPolicy: 'network-only'
  })
})
