<template>
  <div>
    <audio ref="player" controls></audio>
    <h1>Nuxt - Django + SocketIO Test</h1>
    <h2>Send:</h2>
    <form @submit.prevent="emitData">
      <input v-model="formData.emit" type="text" placeholder="Message" />
      <input type="submit" value="Echo" />
    </form>
    <form @submit.prevent="emitBroadcast">
      <input v-model="formData.broadcast" type="text" placeholder="Message" />
      <input type="submit" value="Broadcast" />
    </form>
    <form @submit.prevent="emitJoin">
      <input v-model="formData.joinRoom" type="text" placeholder="Room Name" />
      <input type="submit" value="Join Room" />
    </form>

    <form @submit.prevent="emitLeave">
      <input v-model="formData.leaveRoom" type="text" placeholder="Room Name" />
      <input type="submit" value="Leave Room" />
    </form>

    <form @submit.prevent="emitSendRoom">
      <input
        v-model="formData.sendRoomName"
        type="text"
        placeholder="Room Name"
      />
      <input
        v-model="formData.sendRoomMessage"
        type="text"
        placeholder="Message"
      />
      <input type="submit" value="Send to Room" />
    </form>
    <form @submit.prevent="emitClose">
      <input v-model="formData.closeRoom" type="text" placeholder="Room Name" />
      <input type="submit" value="Close Room" />
    </form>
    <form @submit.prevent="emitDisconnect">
      <input type="submit" value="Disconnect" />
    </form>
    <br />
    <h2>Receive:</h2>
    <div><p ref="log"></p></div>
  </div>
</template>

<script>
import { io } from 'socket.io-client'

export default {
  name: 'IndexComponent',
  components: {},
  data() {
    return {
      formData: {
        emit: '',
        broadcast: '',
        joinRoom: '',
        leaveRoom: '',
        sendRoomName: '',
        sendRoomMessage: '',
        closeRoom: '',
      },
    }
  },
  head() {
    return {
      script: [
        {
          src: 'https://cdnjs.cloudflare.com/ajax/libs/webrtc-adapter/8.1.0/adapter.min.js',
          body: true,
        },
        {
          src: 'js/janus.js',
          body: true,
        },
      ],
    }
  },
  computed: {},
  mounted() {
    this.initSocket()
    this.initJanus()
  },
  created() {},
  methods: {
    initSocket() {
      const that = this
      // eslint-disable-next-line no-undef
      this.socket = io.connect('ws://localhost:8081')
      // this.socket = io.connect({ port: 8081 })

      this.socket.on('connect', function () {
        that.socket.emit('my_event', { data: "I'm connected!" })
      })
      this.socket.on('disconnect', function () {
        that.$refs.log.append('Disconnected')
      })
      this.socket.on('my_response', function (msg) {
        that.$refs.log.append('Received: ' + msg.data)
      })
    },

    initJanus() {
      // eslint-disable-next-line no-undef
      const that = this
      const { hostname, protocol } = window.location
      const server =
        protocol === 'http:'
          ? `http://${hostname}:8088/janus`
          : `https://${hostname}:8089/janus`

      // eslint-disable-next-line no-undef
      const opaqueId = 'streamingtest-' + Janus.randomString(12)
      this.audioElem = this.$refs.player
      // eslint-disable-next-line no-undef
      Janus.init({
        debug: 'all',
        callback: () => {
          // Make sure the browser supports WebRTC
          // eslint-disable-next-line no-undef
          if (!Janus.isWebrtcSupported()) {
            alert('No WebRTC support... ')
            return
          }
          // Create session
          // eslint-disable-next-line no-undef
          that.janus = new Janus({
            server,
            // TODO: needed?
            iceServers: [{ urls: 'stun:stun.l.google.com:19302' }],
            success: () => {
              // Attach to Streaming plugin
              that.janus.attach({
                plugin: 'janus.plugin.streaming',
                opaqueId,
                success: (pluginHandle) => {
                  that.streaming = pluginHandle
                  console.log(
                    'Plugin attached! (' +
                      that.streaming.getPlugin() +
                      ', id=' +
                      that.streaming.getId() +
                      ')'
                  )
                  // Setup streaming session
                  that.updateStreamsList()
                },
                error(error) {
                  console.error('  -- Error attaching plugin... ', error)
                  alert('Error attaching plugin... ' + error)
                },
                iceState(state) {
                  console.log('ICE state changed to ' + state)
                },
                webrtcState(on) {
                  console.log(
                    'Janus says our WebRTC PeerConnection is ' +
                      (on ? 'up' : 'down') +
                      ' now'
                  )
                },
                onmessage(msg, jsep) {
                  console.log(' ::: Got a message :::', msg)
                  if (jsep) {
                    console.log('Handling SDP as well...', jsep)
                    // eslint-disable-next-line unicorn/prefer-includes
                    const stereo = jsep.sdp.indexOf('stereo=1') !== -1
                    // Offer from the plugin, let's answer
                    that.streaming.createAnswer({
                      jsep,
                      // We want recvonly audio/video and, if negotiated, datachannels
                      media: { audioSend: false, videoSend: false, data: true },
                      customizeSdp(jsep) {
                        // eslint-disable-next-line unicorn/prefer-includes
                        if (stereo && jsep.sdp.indexOf('stereo=1') === -1) {
                          // Make sure that our offer contains stereo too
                          jsep.sdp = jsep.sdp.replace(
                            'useinbandfec=1',
                            'useinbandfec=1;stereo=1'
                          )
                        }
                      },
                      success(jsep) {
                        console.log('Got SDP!', jsep)
                        const body = { request: 'start' }
                        that.streaming.send({ message: body, jsep })
                      },
                      error(error) {
                        console.error('WebRTC error:', error)
                        alert('WebRTC error... ' + error.message)
                      },
                    })
                  }
                },
                onremotestream(stream) {
                  console.log(' ::: Got a remote stream :::', stream)
                  // eslint-disable-next-line no-undef
                  Janus.attachMediaStream(that.audioElem, stream)
                  that.audioElem.volume = 1
                },
                oncleanup() {
                  console.log(' ::: Got a cleanup notification :::')
                },
              })
            },
            error(error) {
              console.error(error)
            },
            destroyed() {
              // window.location.reload();
            },
          })
        },
      })
    },
    updateStreamsList() {
      const that = this
      const body = { request: 'list' }
      console.log('Sending message:', body)

      this.streaming.send({
        message: body,
        success(result) {
          if (!result) {
            alert('Got no response to our query for available streams')
            return
          }

          if (result.list) {
            const list = result.list
            console.log('Got a list of available streams')
            console.log(list)
            for (const mp in list) {
              console.log(
                '  >> [' +
                  list[mp].id +
                  '] ' +
                  list[mp].description +
                  ' (' +
                  list[mp].type +
                  ')'
              )
            }

            // start first one
            if (list && list[0]) {
              const body = {
                request: 'watch',
                id: list[0].id,
              }
              console.log(body)
              that.streaming.send({ message: body })
            }
          }
        },
      })
    },

    //  =============================== FORM ===============================
    // event handler for server sent data
    // the data is displayed in the "Received" section of the page
    // handlers for the different forms in the page
    // these send data to the server in a variety of ways

    emitData() {
      // console.log(this.formData.emit)
      this.socket.emit('my_event', { data: this.formData.emit })
    },

    emitBroadcast() {
      // console.log(this.formData.broadcast)
      this.socket.emit('my_broadcast_event', { data: this.formData.broadcast })
    },

    emitJoin() {
      // console.log(this.formData.joinRoom)
      this.socket.emit('join', { data: this.formData.joinRoom })
    },
    emitLeave() {
      // console.log(this.formData.leaveRoom)
      this.socket.emit('leave', { data: this.formData.leaveRoom })
    },

    emitSendRoom() {
      // console.log(this.formData.sendRoomName, this.formData.sendRoomMessage)
      this.socket.emit('my_room_event', {
        room: this.formData.sendRoomName,
        data: this.formData.sendRoomMessage,
      })
    },

    emitClose() {
      // console.log(this.formData.closeRoom)
      this.socket.emit('close_room', { room: this.formData.closeRoom })
    },

    emitDisconnect() {
      console.log('Sending disconnect_request')
      this.socket.emit('disconnect_request')
    },
  },
}
</script>

<style scoped lang="scss"></style>
