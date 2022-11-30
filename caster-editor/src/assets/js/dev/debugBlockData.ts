const debugBlockData = [
  // Markdown
  { cellCode: "<h2> Hello Markdown</h2> <p> this is a markdown cell.</p>", cellOrder: 0, cellType: "markdown", uuid: "51d31f9d-a94d-4edf-9aaf-105267b50130", __typename: "ScriptCell" },

  // python
  { cellCode: "# Use of String Formatting\r\nfloat1 = 563.78453\r\nprint(\"{:5.2f}\".format(float1))\r\n\r\n# Use of String Interpolation\r\nfloat2 = 563.78453\r\nprint(\"%5.2f\" % float2)", cellOrder: 1, cellType: "python", uuid: "ea95186e-a3b6-4008-a84d-97d59d0fe804", __typename: "ScriptCell" },

  // supercollider
  { cellCode: "({RHPF.ar(OnePole.ar(BrownNoise.ar, 0.99), LPF.ar(BrownNoise.ar, 14)\r\n* 400 + 500, 0.03, 0.003)}!2)\r\n+ ({RHPF.ar(OnePole.ar(BrownNoise.ar, 0.99), LPF.ar(BrownNoise.ar, 20)\r\n* 800 + 1000, 0.03, 0.005)}!2)\r\n* 4\r\n}.play", cellOrder: 2, cellType: "supercollider", uuid: "18ea7291-e11a-4f5a-b458-f0bd122edba5", __typename: "ScriptCell" },

  // comment
  { cellCode: "<h2> Hello Comment</h2> <p> this is a <em>basic</em> example of a <strong>comment</strong>. Sure, there are all kind of basic text styles you’d probably expect from a text editor. But wait until you see the lists or anything else you can do via markdown</p>", cellOrder: 3, cellType: "comment", uuid: "1a4a9a65-f5c4-45d2-8ab1-ae392009ab1a", __typename: "ScriptCell" }

];

export { debugBlockData };
