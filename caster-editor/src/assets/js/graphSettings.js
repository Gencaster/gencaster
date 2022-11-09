import * as vNG from 'v-network-graph'

const GraphSettings = {
  standard: vNG.defineConfigs({
    node: {
      selectable: true,
      normal: {
        color: 'lightgrey',
      },
      hover: {
        color: 'black',
      },
      label: {
        fontSize: 14,
      },
    },
    edge: {
      selectable: true,
      normal: {
        width: 3,
        color: 'black',
        dasharray: '0',
        linecap: 'butt',
        animate: false,
        animationSpeed: 50,
      },
      hover: {
        width: 4,
        color: 'black',
        dasharray: '0',
        linecap: 'butt',
        animate: false,
        animationSpeed: 50,
      },
      selected: {
        width: 3,
        color: '#dd8800',
        dasharray: '6',
        linecap: 'round',
        animate: false,
        animationSpeed: 50,
      },
      // gap: 5,
      // type: 'straight',
      type: 'curve',
      gap: 40,
      margin: 2,
      marker: {
        source: {
          type: 'none',
          width: 4,
          height: 4,
          margin: -1,
          units: 'strokeWidth',
          color: null,
        },
        target: {
          type: 'arrow',
          width: 4,
          height: 4,
          margin: -1,
          units: 'strokeWidth',
          color: null,
        },
      },
    },
  }),
}

export { GraphSettings }
