/* eslint-disable */
// import { bindAll } from 'lodash'
import { io } from 'socket.io-client'

export default class ApiSocket {
  constructor(scope) {
    this.params = {}
    this.$config = scope.$config
    this.$store = scope.$store
    this.scope = scope
  }

  init() {
    // console.log('init api socket')
    // console.log(this.$config.SOCKETURL)
    this.startSocket()
  }

  startSocket() {
    const that = this

    this.socket = io(this.$config.SOCKETURL)

    this.socket.io.on('error', (error) => {
      console.log(error)
    })

    this.socket.on('connect', () => {
      // console.log(`connected to server`)
      this.$store.state.socket.id = this.socket.id
      // console.log(`My id is ${this.$store.state.socket.id}`)
      this.$store.state.socket.socketConnected = true
      that.startCommunication()
    })
  }

  startCommunication() {
    this.socket.emit('message', 'hello from client')
  }

  destroy() {
    console.log('ApiSocket destroyed')
  }
}
