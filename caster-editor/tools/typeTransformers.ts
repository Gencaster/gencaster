import {
  Nodes as GraphNodes,
  Node as GraphNode,
  Edges as GraphEdges,
  Edge as GraphEdge
} from 'v-network-graph'
import { Edge as StoryEdge, Node as StoryNode } from '../graphql/graphql'

export function transformEdges(edges: StoryEdge[]): GraphEdges {
  /*
      transforms the edges from our StoryGraph model to
      v-network-graph model. Maybe this can be done in a nicer,
      two way support via urql as some kind of type transformation?
      */
  const e: GraphEdges = {}
  edges.forEach((edge) => {
    const graphEdge: GraphEdge = {
      source: edge.inNode.uuid,
      target: edge.outNode.uuid
    }
    e[edge.uuid] = graphEdge
  })
  console.log('foo')
  const foo = 'hello world'
  console.log(foo)
  console.log(2)
  return e
}

export function transformNodes(nodes: StoryNode[]): GraphNodes {
  const n: GraphNodes = {}
  nodes.forEach((node) => {
    const graphNode: GraphNode = {
      name: node.name
    }
    n[node.uuid] = graphNode
  })
  return n
}
