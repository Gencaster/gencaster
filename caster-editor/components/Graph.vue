<script lang="ts">
import { Nodes as GraphNodes, Node as GraphNode, Edges as GraphEdges, Edge as GraphEdge } from "v-network-graph";
import { defineComponent, toRefs, transformVNodeArgs } from "vue";
import { useQuery } from "@urql/vue";
import { useGetGraphQuery, Edge as StoryEdge, Node as StoryNode } from "../graphql/graphql";
import { propsToAttrMap } from "@vue/shared";
import { transformEdges, transformNodes } from "../tools/typeTransformers"

export default defineComponent({
  props: {
    uuid: String
  },

  setup(props) {
    const uuid = toRefs(props).uuid;
    const result = useGetGraphQuery({
        variables: {uuid: uuid},
        requestPolicy: 'network-only',
    });
    return {
      fetching: result.fetching,
      data: result.data,
      error: result.error,
      transformEdges,
      transformNodes,
    };
  }
});
</script>

    <template>
  <div class="index-page">
    <div v-if="fetching">...Loading</div>
    <div v-else>
      <h1>Welcome to the Editor of <b>{{ data.graph.name }}</b></h1>
      <div class="demo-control-panel">
        <div>
          <label>Node:</label>
          {{ data.graph.nodes.length }}
        </div>
        <div>
          <label>Edge:</label>
          {{ data.graph.edges.length }}
        </div>
      </div>
      <br />
      <v-network-graph
        class="graph"
        :nodes="transformNodes(data.graph.nodes)"
        :edges="transformEdges(data.graph.edges)"
      />
    </div>
  </div>
</template>
