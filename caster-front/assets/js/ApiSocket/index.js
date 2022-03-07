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

    if (socketio.sails) {
      // important so hot reload works
      this.io = socketio
    } else {
      this.io = sailsio(socketio)
    }

    // try to reconnect if connection is lost
    this.io.sails.reconnection = true
    this.io.sails.url = this.$config.SOCKETURL // or process.env.BASE_URL

    // Remember this must match te same array in config/sockets.js (server config)
    this.io.sails.transports = ['websocket']

    // this.io.socket.on('connect', function () {
    //   console.log('connectedgsdg')
    //   // io.socket.get('/join', function serverResponded(body, JWR) {
    //   //   // body === JWR.body
    //   //   console.log('Sails responded with: ', body)
    //   //   console.log('with headers: ', JWR.headers)
    //   //   console.log('and with status code: ', JWR.statusCode)

    //   //   // When you are finished with `io.socket`, or any other sockets you connect manually,
    //   //   // you should make sure and disconnect them, e.g.:
    //   //   //io.socket.disconnect();

    //   //   // (note that there is no callback argument to the `.disconnect` method)
    //   // })
    // })

    // console.log(this.io)
    // console.log(this.io.socket)
    // console.log(this.io.sails)

    this.io.socket.on('connect', function onConnect() {
      console.log('This socket is now connected to the Sails server.')
    })

    this.io.socket.on('hello', function (broadcastedData) {
      console.log(data.howdy)
      // => 'hi there!'
    })

    this.io.socket.on('connect', function (broadcastedData) {
      console.log(data.howdy)
      // => 'hi there!'
    })

    this.io.socket.get('/hello', (resData, jwres) => {
      console.log('test')
      // this.setState({
      //   sessions: resData.sessions,
      //   loaded: true,
      // })
    })

    // this.io.socket.on('hello', function (data) {
    //   console.log('Socket `' + data.id + '` joined the party!')
    // })

    // this.io.socket.get('SAILS ENDPOINT WHICH HANDLE SOCKET', function (data) {
    //   console.log('Socket Data', data)
    // })

    // this.io.socket.get('hello', function (data) {
    //   console.log('Socket Data', data)
    // })

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
