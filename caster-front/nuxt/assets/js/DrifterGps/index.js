/* eslint-disable */

// MAPBOX USES long,lat
// GEOJSON long, lat
// GOOGLE USES lat, long

// import { bindAll } from 'lodash'
// eslint-disable-next-line no-unused-vars
import gpsSimulation from '~/assets/json/gps-simulations-latlong.json'

export default class DrifterGps {
  constructor(scope) {
    this.params = {
      customGpsData: [],
      currentIndex: 0,
      keepSimulationRunning: false,
      loopSimulation: false,

      runningRealGPS: false,

      logPosition: false,
    }

    this.gpsOptions = {
      enableHighAccuracy: true,
      // timeout: 5000,
      maximumAge: 0, //not allowed to use cached https://developer.mozilla.org/en-US/docs/Web/API/PositionOptions/maximumAge
      //timeout: 1000, // in ms
      // desiredAccuracy: 0,
      frequency: 1,
    }

    this.scope = scope
  }

  init() {}

  start(source, speed, loop) {
    if (source === 'own') {
      this.accessGPS()
    } else {
      this.startSimulation(source, speed, loop)
    }
  }

  stop() {
    if (!this.params.runningRealGPS) {
      this.params.keepSimulationRunning = false
      this.params.loopSimulation = false
    }

    if (this.params.runningRealGPS) {
      navigator.geolocation.clearWatch(this.params.geolocationWatchId)
      this.params.runningRealGPS = false
    }
  }

  accessGPS() {
    if (navigator.geolocation) {
      this.params.geolocationWatchId = navigator.geolocation.watchPosition(
        this.newRealPosition.bind(this),
        this.geoError,
        this.gpsOptions
      )
    } else {
      this.scope.$router.push('/gps-instructions')
    }
  }

  geoError() {
    this.scope.$router.push('/blocked-gps')
  }

  newRealPosition(position) {
    this.params.runningRealGPS = true

    if (this.params.logPosition) {
      console.log(position)
    }

    this.scope.newPosition(position)
  }

  startSimulation(source, speed, loop) {
    this.params.customGpsData[0] // empty current
    this.params.currentIndex = 0

    if ((gpsSimulation.params.order = 'latlong')) {
      gpsSimulation.data[source].forEach((c) => {
        this.params.customGpsData.push([c[1], c[0]])
      })
    } else {
      this.params.customGpsData = gpsSimulation.data[source]
    }

    if (loop === 'yes') {
      this.params.loopSimulation = true
    }

    this.params.keepSimulationRunning = true
    this.simulateGPS(speed)
  }

  simulateGPS(speed) {
    const that = this
    const coordinates = this.params.customGpsData[this.params.currentIndex]
    this.params.currentIndex++
    if (this.params.currentIndex >= this.params.customGpsData.length) {
      if (this.params.loopSimulation) {
        this.params.currentIndex = 0
      } else {
        this.params.keepSimulationRunning = false // to end on end
        console.log('stopped gps loop')
      }
    }

    const gpsObj = {
      coords: {
        latitude: coordinates[1],
        longitude: coordinates[0],
      },
      timestamp: new Date(),
    }

    this.scope.newPosition(gpsObj)

    setTimeout(() => {
      if (that.params.keepSimulationRunning) {
        that.simulateGPS(speed)
      }
    }, speed * 1000)
  }

  destroy() {
    console.log('GPS destroyed')
  }

  // dev functions
  getSimulatedGPSData() {
    return gpsSimulation.data
  }

  // async exportBandImgAsync() {
  //   return new Promise((resolve, reject) => {
  //     const self = this
  //     this.generateOffsetRenderDiv()

  //     const options = {
  //       width: 1024,
  //       height: 1024,
  //       // windowWidth: 1024,
  //       // windowWidth: 1024,
  //       backgroundColor: null,
  //       scale: 1,
  //     }

  //     html2canvas(this.dom.renderDiv, options).then(function (canvas) {
  //       self.hideRenderDiv()
  //       let imgData = canvas.toDataURL('image/png', 0.7)
  //       // let canvasCtx = canvas.getContext('2d')

  //       let generatedImage = new Image()
  //       generatedImage.onload = function () {
  //         resolve(generatedImage)
  //       }
  //       generatedImage.src = imgData
  //     })
  //   })
  // }
}
