export const strict = false

export const state = () => ({
  version: 0.01,
  userData: {
    username: null,
  },
  audio: {
    isPlaying: false,
  },
  gps: {
    gpsRunning: false,
  },
  socket: {
    socketConnected: false,
    socketOffline: null,
    id: null,
  },
  // io: {}, // heißt schon io
})

export const mutations = {
  // increment(state) {
  //   state.counter++
  // },
}
