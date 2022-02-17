<template>
  <section>
    <p>frontend.gencast.augmented.audio</p>

    <p v-if="params.socketConnected">Connected to server</p>
  </section>
</template>

<script>
import { io } from 'socket.io-client'
export default {
  data() {
    return {
      params: {
        socketConnected: false,
        socketOffline: null,
        socketURL: this.$config.SOCKETURL,
      },
    }
  },
  computed: {},
  mounted() {
    this.init()
  },
  created() {},
  methods: {
    init() {
      this.startSocket()
    },
    startSocket() {
      const that = this
      this.socket = io(this.params.socketURL)
      this.socket.io.on('error', (error) => {
        console.log(error)
      })

      this.socket.on('connect', () => {
        console.log(`connected to server`)
        console.log(`My id is ${this.socket.id}`)
        this.params.socketConnected = true
        that.startCommunication()
      })
    },

    startCommunication() {
      this.socket.emit('message', 'hello from client')
    },
  },
}
</script>

<style lang="scss"></style>
