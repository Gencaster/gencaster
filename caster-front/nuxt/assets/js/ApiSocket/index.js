/* eslint-disable */
// import { bindAll } from 'lodash'
import socketio from 'socket.io-client'
import sailsio from 'sails.io.js'

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

    // this.socket = io(this.$config.SOCKETURL)

    this.socket = sailsio(socketio)

    // try to reconnect if connection is lost
    this.socket.sails.reconnection = true

    this.socket.sails.url = 'http://localhost:1337' // or process.env.BASE_URL
    // Remember this must match te same array in config/sockets.js (server config)
    this.socket.sails.transports = ['websocket']

    // this.socket.io.on('error', (error) => {
    //   console.log(error)
    // })

    // this.socket.on('connect', () => {
    //   // // console.log(`connected to server`)
    //   // this.$store.state.socket.id = this.socket.id
    //   // // console.log(`My id is ${this.$store.state.socket.id}`)
    //   // this.$store.state.socket.socketConnected = true
    //   // that.startCommunication()
    // })
  }

  startCommunication() {
    this.socket.emit('message', 'hello from client')
  }

  destroy() {
    console.log('ApiSocket destroyed')
  }
}
