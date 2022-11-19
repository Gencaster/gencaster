import type { Edge as GraphEdge, Edges as GraphEdges, Node as GraphNode, Nodes as GraphNodes } from "v-network-graph";
import type { Edge as StoryEdge, Node as StoryNode } from "../graphql/graphql";

export function transformEdges(edges: StoryEdge[]): GraphEdges {
  /*
    transforms the edges from our StoryGraph model to
    v-network-graph model. Maybe this can be done in a nicer,
    two way support via urql as some kind of type transformation?
    */
  const e: GraphEdges = {};
  edges.forEach((edge) => {
    const graphEdge: GraphEdge = {
      source: edge.inNode.uuid,
      target: edge.outNode.uuid
    };
    e[edge.uuid] = graphEdge;
  });
  return e;
}

export function transformNodes(nodes: StoryNode[]): GraphNodes {
  const n: GraphNodes = {};
  nodes.forEach((node) => {
    const graphNode: GraphNode = {
      name: node.name,
      color: node.color,
      scriptCells: node.scriptCells
    };
    n[node.uuid] = graphNode;
  });
  return n;
}

export function transformLayout(nodes: StoryNode[]): GraphNodes {
  const n: GraphNodes = {};
  nodes.forEach((node) => {
    const graphNode: GraphNode = {
      x: node.positionX,
      y: node.positionY
    };
    n[node.uuid] = graphNode;
  });
  const layout = {
    nodes: n
  };
  return layout;
}
