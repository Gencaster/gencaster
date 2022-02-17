<template>
  <section>
    <nav>
      <div class="left"><p>blocked-gps</p></div>
      <div class="right">
        <p>v {{ $store.state.version }}</p>
      </div>
    </nav>
    <div class="nav-spacer"></div>

    <div class="desc">
      Oops, you seem to have declined gps access or something else went wrong.
      Please return and try again. <br />
      <br />Take a look at the <NuxtLink to="/">GPS instructions</NuxtLink> or
      <NuxtLink to="/">Restart</NuxtLink>.
    </div>
  </section>
</template>

<script>
// import SlideUpDown from 'vue-slide-up-down'

export default {
  components: {
    //   SlideUpDown,
  },
  data() {
    return {
      // dropdowns: {
      //   android: true,
      //   ios: true,
      // },
    }
  },

  computed: {},
  mounted() {},
  created() {},
  onDestroy() {},
  methods: {},
}
</script>

<style lang="scss" scoped>
select,
input {
  font-size: 15px;
}

nav {
  background-color: $lightweight;
  height: 30px;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 10;
  padding: 0 10px 0 10px;

  display: flex;
  justify-content: center;
  align-items: center;
  border-bottom: 1px solid black;

  p::v-deep {
    font-size: 16px;
  }

  .left {
    width: 50%;
  }

  .right {
    width: 50%;
    display: flex;
    justify-content: flex-end;
  }
}

p {
  font-size: 16px;
}

.nav-spacer {
  position: relative;
  background-color: $lightweight;
  height: 30px;
  width: 100%;
  display: block;
  margin: 0;
  padding: 0;
  margin-bottom: 10px;
}

.general-btn {
  margin-right: 10px;
  background-color: black;
  margin-bottom: 10px;
  display: inline-block;
  margin: 0;

  p {
    font-size: 15px;
    color: $lightweight;
    padding: 1px 8px 3px 8px;
  }
}

.shortcuts {
  padding: 0 10px 0 10px;
  width: 100%;
  position: relative;
  display: flex;
  flex-wrap: wrap;

  .general-btn {
    margin-bottom: 10px;
    margin-right: 10px;
  }

  .general-btn:last-child {
    margin-right: 0px;
  }
}

.desc {
  padding: 12px 10px 0 10px;
  width: 100%;
  position: relative;

  font-size: 18px;

  margin-bottom: 24px;

  a {
    color: $black;
    font-size: 18px;
  }
}

.dropdown {
  padding: 0 10px 0 10px;
  width: 100%;
  height: auto;
  position: relative;
  margin-bottom: 10px;

  p {
    // font-size: 15px;
  }

  .content {
    ::v-deep p,
    ::v-deep span {
      font-size: 15px;
    }

    border: 1px solid black;
    border-top: 0px;

    .cell {
      width: 100%;
      padding: 0 6px 0 6px;
      border-bottom: solid 1px black;
      height: 40px;

      display: flex;

      &.button-line {
        justify-content: space-between;
        align-items: center;
      }

      &.text-line {
        justify-content: space-between;
        align-items: center;
        .text {
          height: 20px;
          width: 50%;

          input {
            display: flex;
            height: 20px;
            width: 100%;
            font-size: 15px;
            border: 0;

            text-align: right;
          }
        }
      }

      &.content-line {
        justify-content: space-between;
        align-items: center;
        display: flex;
        flex-direction: column;
        height: auto;
      }

      &.select-line {
        justify-content: space-between;
        align-items: center;

        select {
          display: inline-flex;
          white-space: pre-wrap;
          text-align: right;
        }
      }

      &.select-number {
        justify-content: space-between;
        align-items: center;
      }
    }

    .cell:last-child {
      border-bottom: 0px;
    }
  }

  .header {
    width: 100%;
    height: 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;

    border: solid black 1px;
    padding: 0 6px 0 6px;

    .drop-button {
      width: 20px;
      height: 20px;
      display: block;
    }

    p {
      display: inline-block;
      font-size: 15px;
      line-height: 18px;

      span {
        position: absolute;
        transform-origin: center;
        font-size: 15px;
        transform: rotate(0deg);
        transition: all 0.5s cubic-bezier(0.87, 0, 0.13, 1);

        height: 20px;

        &.active {
          transform: rotate(180deg);
        }
      }
    }
  }
}

// special dropdowns
.mapboxgl-ctrl-attrib-inner {
  font-size: 12px !important;

  a {
    font-size: 12px !important;
  }
}

.mapboxgl-ctrl-attrib::v-deep {
  display: none;
  color: red;
  font-size: 12px !important;
}

.dropdown {
  .map-wrapper {
    width: 100%;
    height: 40vh;

    .mapboxgl-ctrl-geolocate::v-deep,
    .mapboxgl-ctrl-top-right::v-deep {
      display: none !important;
      opacity: 0.1 !important;
    }
  }
}

.status-bar {
  position: fixed;
  bottom: 0px;
  left: 0;
  width: 100%;
  height: auto;
  z-index: 10;
  background-color: $lightweight;
  border-top: solid 1px black;

  padding: 0 6px 0 6px;
  background-color: black;

  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;

  p {
    margin: 0;
    padding: 0;
    display: inline-block;
    width: auto;
    height: 20px;
    margin-right: 10px;
    font-size: 10px;
    line-height: 20px;
    color: white;
    margin-bottom: 2px;
  }
}
</style>
