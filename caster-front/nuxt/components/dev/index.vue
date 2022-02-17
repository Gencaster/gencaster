<template>
  <section class="dev-page">
    <nav>
      <div class="left"><p>beta.gencaster</p></div>
      <div class="right">
        <p>v {{ $store.state.version }}</p>
      </div>
    </nav>
    <div class="nav-spacer"></div>

    <div class="shortcuts">
      <div v-if="!$store.state.audio.isPlaying" class="general-btn">
        <p>▶ Play</p>
      </div>
      <div v-if="$store.state.audio.isPlaying" class="general-btn">
        <p>■ Stop</p>
      </div>
      <div class="general-btn">
        <p @click="startGps">↑ Start gps</p>
      </div>
      <div class="general-btn">
        <p>↻ Reset Game</p>
      </div>
    </div>

    <div class="dropdown">
      <div class="header">
        <p>Personal Data</p>
        <p
          class="drop-button"
          @click="dropdowns.personalData = !dropdowns.personalData"
        >
          <span :class="{ active: !dropdowns.personalData }">▼</span>
        </p>
      </div>
      <slide-up-down
        class="content"
        :active="dropdowns.personalData"
        :duration="300"
      >
        <div class="cell text-line">
          <p>Name</p>
          <div class="text">
            <input
              id="username"
              type="text"
              value="Vinzenz"
              placeholder="Your Name"
              @change="usernameUpdate"
              @keyup="usernameUpdate"
            />
          </div>
        </div>
      </slide-up-down>
    </div>
    <div class="dropdown">
      <div class="header">
        <p>GPS</p>
        <p class="drop-button" @click="dropdowns.gps = !dropdowns.gps">
          <span :class="{ active: !dropdowns.gps }">▼</span>
        </p>
      </div>
      <slide-up-down class="content" :active="dropdowns.gps" :duration="300">
        <div class="cell button-line">
          <p>Launch Gps</p>
          <div v-if="!dev.gpsStarted" class="general-btn" @click="startGps">
            <p>start</p>
          </div>
          <div v-if="dev.gpsStarted" class="general-btn" @click="stopGps">
            <p>stop</p>
          </div>
        </div>
        <div class="cell select-line">
          <p>Source</p>
          <div class="select">
            <select id="gpsSelectDropdown" name="gps">
              <option value="own">Device</option>
            </select>
          </div>
        </div>
        <div class="cell select-number">
          <p>Seconds per push</p>
          <div class="wrapper">
            <input
              id="secondsPerPush"
              type="number"
              name="quantity"
              min="0.1"
              max="60"
              value="0.5"
            />
          </div>
        </div>
        <div class="cell select-number">
          <p>Loop Simulation</p>
          <div class="wrapper">
            <select id="loopSimulation">
              <option value="yes">Yes</option>
              <option value="no" selected>No</option>
            </select>
          </div>
        </div>
        <!-- <div class="cell button-line">
          <p>Start Gps</p>
          <div class="general-btn"><p>start</p></div>
        </div> -->
      </slide-up-down>
    </div>

    <div class="dropdown">
      <div class="header">
        <p>GPS Data</p>
        <p class="drop-button" @click="dropdowns.gpsdata = !dropdowns.gpsdata">
          <span :class="{ active: !dropdowns.gpsdata }">▼</span>
        </p>
      </div>
      <slide-up-down
        class="content"
        :active="dropdowns.gpsdata"
        :duration="300"
      >
        <div class="cell button-line">
          <p>Last Coordinates</p>
          <p>{{ dev.positionhr }}</p>
        </div>
        <div class="cell button-line">
          <p>Last timestamp</p>
          <p>{{ dev.timestamphr }}</p>
        </div>
      </slide-up-down>
    </div>

    <div class="dropdown">
      <div class="header">
        <p>Map</p>
        <p class="drop-button" @click="dropdowns.mapbox = !dropdowns.mapbox">
          <span :class="{ active: !dropdowns.mapbox }">▼</span>
        </p>
      </div>
      <slide-up-down class="content" :active="dropdowns.mapbox" :duration="300">
        <div class="map-wrapper">
          <client-only>
            <MglMap
              :access-token="dev.accessToken"
              :map-style="dev.mapStyle"
              :center="playerdata.position"
              :zoom="dev.zoom"
              @load="onMapLoaded"
            >
              <!-- <MglMarker :coordinates="dev.center" color="blue" /> -->
              <!-- <MglMarker :coordinates="dev.center"> </MglMarker> -->

              <MglGeojsonLayer
                :source-id="devMap.geoJsonSource.data.id"
                :source="devMap.geoJsonSource"
                layer-id="playerID"
                :layer="devMap.geoJsonlayer"
              />
            </MglMap>
          </client-only>
        </div>
      </slide-up-down>
    </div>

    <div class="status-bar">
      <p v-if="$store.state.socket.socketConnected">Socket ✓</p>
      <p v-if="$store.state.socket.socketConnected">
        {{ $store.state.socket.id }}
      </p>
      <p v-if="$store.state.gps.gpsRunning">GPS Running</p>
    </div>

    <div class="spacer"></div>
  </section>
</template>

<script>
import SlideUpDown from 'vue-slide-up-down'

// import { MglMap, MglMarker } from 'vue-mapbox'
import DrifterGps from '~/assets/js/DrifterGps'
import ApiSocket from '~/assets/js/ApiSocket'
import Helpers from '~/assets/js/Helpers'

export default {
  components: {
    SlideUpDown,
  },
  data() {
    return {
      playerdata: {
        position: [13.429730074111301, 52.49331177086796],
        timestamp: null,
      },
      dev: {
        active: true, // is the dev stuff active like map and so on
        simulatedGPSData: null,
        gpsStarted: false,

        // interface
        positionhr: 'null',
        timestamphr: 'null',

        // mapbox
        accessToken:
          'pk.eyJ1Ijoidmlubm5pIiwiYSI6ImNrc3lrY2IzZTFxaXYyb2xzOGZ6ZzhidjYifQ.7gf6hMmd9pEbfPlMJZDB6w', // your access token. Needed if you using Mapbox maps
        mapStyle: 'mapbox://styles/vinnni/cksylkcv06wd818o2syr9mjrm', // your map style,
        zoom: 15,
      },
      devMap: {
        geoJsonSource: {
          type: 'geojson',
          data: {
            id: 'playerID',
            type: 'Feature',
            geometry: {
              type: 'Point',
              coordinates: [13.429730074111301, 52.49331177086796],
            },
            properties: {
              name: 'Player Point',
            },
          },
        },
        geoJsonlayer: {
          type: 'circle',
          paint: {
            'circle-color': '#ff0000',
          },
        },
      },
      dropdowns: {
        personalData: true,
        gps: true,
        gpsdata: true,
        mapbox: true,
      },
    }
  },
  head: {
    link: [
      {
        rel: 'stylesheet',
        href: 'https://api.mapbox.com/mapbox-gl-js/v1.10.0/mapbox-gl.css',
      },
    ],
  },
  computed: {},
  mounted() {
    this.$store.state.userData.username = document.getElementById(
      'username'
    ).value

    this.h = new Helpers()

    this.gps = new DrifterGps(this)
    this.gps.init()

    this.apiSocket = new ApiSocket(this)
    this.apiSocket.init()

    this.runDevSetup()
  },
  created() {
    this.map = null
  },
  onDestroy() {
    this.gps.destroy()
    this.apiSocket.destroy()
  },
  methods: {
    // gps handling
    newPosition(gpsObj) {
      const coordinates = [gpsObj.coords.longitude, gpsObj.coords.latitude]

      this.playerdata.position = coordinates
      this.devMap.geoJsonSource.data.geometry.coordinates = coordinates

      // interface
      this.dev.positionhr = `${Math.round(coordinates[0] * 100000) / 100000},${
        Math.round(coordinates[1] * 100000) / 100000
      }`

      this.dev.timestamphr = this.h.hrtimestamp(gpsObj.timestamp)

      //       this.gpsData.markerGeojson.features[0].geometry.coordinates = [
      //   newlong,
      //   newlat,
      // ];
      // this.map.getSource('locationmarker').setData(this.gpsData.markerGeojson);

      // console.log(this.map)

      // this.map.flyTo({
      //   zoom: this.dev.zoom,
      //   center: coordinates,
      // })
    },

    usernameUpdate() {
      this.$store.state.userData.username = document.getElementById(
        'username'
      ).value
    },

    startGps() {
      this.dev.gpsStarted = true

      const selection = document.getElementById('gpsSelectDropdown').value
      const speed = parseFloat(document.getElementById('secondsPerPush').value)
      const loop = document.getElementById('loopSimulation').value

      this.gps.start(selection, speed, loop)
    },

    stopGps() {
      this.gps.stop()
    },

    runDevSetup() {
      this.fillCustomGps()
    },

    fillCustomGps() {
      this.dev.simulatedGPSData = this.gps.getSimulatedGPSData()
      const select = document.getElementById('gpsSelectDropdown')
      Object.keys(this.dev.simulatedGPSData).forEach((key) => {
        const opt = document.createElement('option')
        opt.value = key
        opt.innerHTML = key
        select.appendChild(opt)
      })
    },

    onMapLoaded(event) {
      console.log('map loaded ')
      // in component
      // this.map = event.map;
      // or just to store if you want have access from other components
      this.$store.map = event.map
      this.map = this.$store.map
    },
  },
}
</script>
