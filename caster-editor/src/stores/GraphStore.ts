import { defineStore } from "pinia";
import type { Ref } from "vue";
import type { Edge as GraphEdge, Edges as GraphEdges, Node as GraphNode, Nodes as GraphNodes } from "v-network-graph";
import type { GraphSubscription, NodeCreate } from "@/graphql/graphql";
import {
  useCreateEdgeMutation,
  useCreateNodeMutation,
  useDeleteEdgeMutation,
  useDeleteNodeMutation,
  useGraphSubscription,
  useUpdateNodeMutation
} from "@/graphql/graphql";

export const useGraphStore = defineStore("graph", () => {
  const uuid: Ref<string> = ref("");

  const { data: graph, error, fetching } = useGraphSubscription({ variables: { uuid }, pause: false });

  // data operations
  const { executeMutation: createNodeMutation } = useCreateNodeMutation();
  const addNode = async (nodeVariables: NodeCreate) => {
    await createNodeMutation(nodeVariables);
  };

  const { executeMutation: deleteNodeMutation } = useDeleteNodeMutation();
  const deleteNode = async (nodeUuid: string) => {
    await deleteNodeMutation({ nodeUuid }).then(async () => {
      console.log(`Deleted node ${nodeUuid}`);
    });
  };

  const { executeMutation: deleteEdgeMutation } = useDeleteEdgeMutation();
  const deleteEdge = async (edgeUuid: string) => {
    await deleteEdgeMutation({ edgeUuid }).then(() => {
      console.log(`Deleted edge ${edgeUuid}`);
    });
  };

  const { executeMutation: createEdgeMutation } = useCreateEdgeMutation();
  const createEdge = async (nodeInUuid: string, nodeOutUuid: string) => {
    await createEdgeMutation({ nodeInUuid, nodeOutUuid }).then((result) => {
      console.log(`Created new edge ${result.data?.addEdge}`);
    });
  };

  const { executeMutation: updateNodeMutation } = useUpdateNodeMutation();
  const updateNodePosition = async (node: GraphSubscription["graph"]["nodes"][0]) => {
    // @todo use an input type in the gql backend
    await updateNodeMutation({
      nodeUuid: node.uuid,
      ...node
    });
  };

  /*
    transforms the edges, nodes and layout from our StoryGraph model to
    v-network-graph model. Maybe this can be done in a nicer,
    two way support via urql as some kind of type transformation?
  */
  function nodes(): GraphNodes {
    const n: GraphNodes = {};
    graph.value?.graph.nodes.forEach((node) => {
      const graphNode: GraphNode = {
        name: node.name,
        color: node.color,
        scriptCells: node.scriptCells
      };
      n[node.uuid] = graphNode;
    });
    return n;
  }

  function edges(): GraphEdges {
    const e: GraphEdges = {};
    graph.value?.graph.edges.forEach((edge) => {
      const graphEdge: GraphEdge = {
        source: edge.inNode.uuid,
        target: edge.outNode.uuid
      };
      e[edge.uuid] = graphEdge;
    });
    return e;
  }

  function layouts(): GraphNodes {
    const n: GraphNodes = {};
    graph.value?.graph.nodes.forEach((node) => {
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

  return {
    graph,
    uuid,
    error,
    fetching,
    nodes,
    edges,
    layouts,
    addNode,
    deleteNode,
    deleteEdge,
    createEdge,
    updateNodePosition
  };
});
