import { defineStore } from "pinia";
import type { Ref } from "vue";
import type { Edge as GraphEdge, Edges as GraphEdges, Node as GraphNode, Nodes as GraphNodes } from "v-network-graph";
import type { GetGraphQuery, NodeCreate } from "@/graphql/graphql";
import {
  useCreateEdgeMutation,
  useCreateNodeMutation,
  useDeleteEdgeMutation,
  useDeleteNodeMutation,
  useGetGraphQuery,
  useUpdateNodeMutation
} from "@/graphql/graphql";

export const useGraphStore = defineStore("graph", () => {
  const graph: Ref<GetGraphQuery["graph"]> = ref({} as GetGraphQuery["graph"]);
  const fetching: Ref<boolean> = ref(true);

  async function getGraph(graphUuid: string) {
    console.log("Get/reload graph from server");
    const { data, fetching: isFetching } = await useGetGraphQuery({ variables: { uuid: graphUuid } }).executeQuery();
    if (data.value?.graph)
      graph.value = data.value.graph;
    fetching.value = isFetching.value;
  }

  const reloadFromServer = async () => {
    await getGraph(graph.value.uuid);
  };

  // data operations
  const { executeMutation: createNodeMutation } = useCreateNodeMutation();
  const addNode = async (nodeVariables: NodeCreate) => {
    await createNodeMutation(nodeVariables);
    await reloadFromServer();
  };

  const { executeMutation: deleteNodeMutation } = useDeleteNodeMutation();
  const deleteNode = async (nodeUuid: string) => {
    await deleteNodeMutation({ nodeUuid }).then(async () => {
      console.log(`Deleted node ${nodeUuid}`);
    });
    await reloadFromServer();
  };

  const { executeMutation: deleteEdgeMutation } = useDeleteEdgeMutation();
  const deleteEdge = async (edgeUuid: string) => {
    await deleteEdgeMutation({ edgeUuid }).then(() => {
      console.log(`Deleted edge ${edgeUuid}`);
    });
    await reloadFromServer();
  };

  const { executeMutation: createEdgeMutation } = useCreateEdgeMutation();
  const createEdge = async (nodeInUuid: string, nodeOutUuid: string) => {
    await createEdgeMutation({ nodeInUuid, nodeOutUuid }).then((result) => {
      console.log(`Created new edge ${result.data?.addEdge}`);
    });
    await reloadFromServer();
  };

  const { executeMutation: updateNodeMutation } = useUpdateNodeMutation();
  const updateNodePosition = (node: GetGraphQuery["graph"]["nodes"][0]) => {
    updateNodeMutation({
      nodeUuid: node.uuid,
      ...node
    });
    reloadFromServer();
  };

  // // watch an array
  // watch(() => graph.value.nodes, (v) => {
  //   console.log(`New len is ${v}`);
  //   for (let i = 0; i < v.length; i++) {
  //     watch(() => graph.value.nodes[i], () => {
  //       console.log(`Changed node ${i}`);
  //     }, { deep: true });
  //   }
  // }, { deep: false });

  /*
    transforms the edges, nodes and layout from our StoryGraph model to
    v-network-graph model. Maybe this can be done in a nicer,
    two way support via urql as some kind of type transformation?
  */
  function nodes(): GraphNodes {
    const n: GraphNodes = {};
    graph.value.nodes.forEach((node) => {
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
    graph.value.edges.forEach((edge) => {
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
    graph.value.nodes.forEach((node) => {
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
    getGraph,
    nodes,
    edges,
    layouts,
    fetching,
    addNode,
    deleteNode,
    deleteEdge,
    createEdge,
    updateNodePosition,
    reloadFromServer
  };
});
