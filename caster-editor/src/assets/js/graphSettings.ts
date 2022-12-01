import * as vNG from "v-network-graph";
import variables from "@/assets/scss/variables.module.scss";

const GraphSettings = {
  standard: vNG.defineConfigs({
    node: {
      selectable: true,
      normal: {
        type: "circle",
        radius: 16,
        strokeWidth: 0,
        color: variables.grey
      },
      hover: {
        type: "circle",
        radius: 16,
        strokeWidth: 0,
        color: variables.greenLight
      },
      selected: {
        type: "circle",
        radius: 16,
        strokeWidth: 0,
        color: variables.greenLight
      },
      label: {
        fontSize: 15,
        fontFamily: "arial",
        color: variables.black,
        margin: 4,
        background: {
          visible: true,
          color: variables.white,
          padding: {
            vertical: 1,
            horizontal: 4
          },
          borderRadius: 2
        }
      },
      focusring: { visible: false },
      zOrder: {
        enabled: true, // whether the z-order control is enable or not. default: false
        bringToFrontOnHover: true, // whether to bring to front on hover.    default: true
        bringToFrontOnSelected: true // whether to bring to front on selected. default: true
      }
    },
    edge: {
      selectable: true,
      normal: {
        width: 3,
        color: "black",
        dasharray: 0,
        animationSpeed: 5,
        linecap: "square",
        animate: false
      },
      hover: {
        width: 4,
        color: variables.greenLight,
        dasharray: "0",
        linecap: "square",
        animate: false
      },
      selected: {
        width: 3,
        color: variables.greenLight,
        dasharray: "0",
        linecap: "square",
        animate: false
      },
      gap: 5,
      // type: "straight",
      type: "curve",
      // gap: 40,
      margin: 8,
      marker: {
        source: {
          type: "none",
          width: 4,
          height: 4,
          margin: -1,
          units: "strokeWidth",
          color: null
        },
        target: {
          type: "arrow",
          width: 4,
          height: 6,
          margin: -1,
          units: "strokeWidth",
          color: null
        }
      },
      zOrder: {
        enabled: true, // whether the z-order control is enable or not. default: false
        bringToFrontOnHover: true, // whether to bring to front on hover.    default: true
        bringToFrontOnSelected: true // whether to bring to front on selected. default: true
      }
    },
    view: {
      grid: {
        visible: false,
        interval: 30,
        thickIncrements: 0,
        line: {
          color: "#F5F5F5",
          width: 1,
          dasharray: 0
        },
        thick: {
          color: "#F5F5F5",
          width: 1,
          dasharray: 0
        }
      }
      // layoutHandler: new vNG.GridLayout({ grid: 30 })
    }
  })
};

export { GraphSettings };
