import type { Node, ScriptCell } from "@/graphql/graphql";
import { CellType } from "@/graphql/graphql";

const emptyNode: Node = {
  color: "blue",
  inEdges: [],
  name: "debugnode",
  outEdges: [],
  positionX: 0,
  positionY: 0,
  scriptCells: [],
  uuid: "debugnode"
};

const debugScriptCells: ScriptCell[] = [
  // Markdown
  {
    node: emptyNode,
    cellCode: `{
    "time" : 1670853882563,
    "blocks" : [
        {
            "id" : "6E_VlpCZln",
            "type" : "header",
            "data" : {
                "text" : "Markdown",
                "level" : 2
            }
        },
        {
            "id" : "OZJfywswBs",
            "type" : "paragraph",
            "data" : {
                "text" : "Hey, this is a little markdown."
            }
        }
    ],
    "version" : "2.26.0"
}`,
    cellOrder: 0,
    cellType: CellType.Markdown,
    uuid: "51d31f9d-a94d-4edf-9aaf-105267b50130",
    __typename: "ScriptCell"
  },

  // python
  { node: emptyNode, cellCode: "# Use of String Formatting\r\nfloat1 = 563.78453\r\nprint(\"{:5.2f}\".format(float1))\r\n\r\n# Use of String Interpolation\r\nfloat2 = 563.78453\r\nprint(\"%5.2f\" % float2)", cellOrder: 1, cellType: CellType.Python, uuid: "ea95186e-a3b6-4008-a84d-97d59d0fe804", __typename: "ScriptCell" },

  // supercollider
  { node: emptyNode, cellCode: "({RHPF.ar(OnePole.ar(BrownNoise.ar, 0.99), LPF.ar(BrownNoise.ar, 14)\r\n* 400 + 500, 0.03, 0.003)}!2)\r\n+ ({RHPF.ar(OnePole.ar(BrownNoise.ar, 0.99), LPF.ar(BrownNoise.ar, 20)\r\n* 800 + 1000, 0.03, 0.005)}!2)\r\n* 4\r\n}.play", cellOrder: 2, cellType: CellType.Supercollider, uuid: "18ea7291-e11a-4f5a-b458-f0bd122edba5", __typename: "ScriptCell" },

  // comment
  {
    node: emptyNode,
    cellCode: `{
    "time" : 1670853951122,
    "blocks" : [
        {
            "id" : "lfuQKy6f3l",
            "type" : "header",
            "data" : {
                "text" : "Comment",
                "level" : 2
            }
        },
        {
            "id" : "OZJfywswBs",
            "type" : "paragraph",
            "data" : {
                "text" : "Hey, this is a little comment."
            }
        }
    ],
    "version" : "2.26.0"
}`,
    cellOrder: 3,
    cellType: CellType.Comment,
    uuid: "1a4a9a65-f5c4-45d2-8ab1-ae392009ab1a",
    __typename: "ScriptCell"
  }

];

export { debugScriptCells, emptyNode };
