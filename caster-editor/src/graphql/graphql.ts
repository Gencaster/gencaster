import gql from 'graphql-tag';
import * as Urql from '@urql/vue';
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
export type Omit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>;
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: string;
  String: string;
  Boolean: boolean;
  Int: number;
  Float: number;
  DateTime: any;
  UUID: any;
  Void: any;
};

/** An enumeration. */
export enum CellType {
  Comment = 'COMMENT',
  Markdown = 'MARKDOWN',
  Python = 'PYTHON',
  Supercollider = 'SUPERCOLLIDER'
}

export type Edge = {
  __typename?: 'Edge';
  inNode: Node;
  outNode: Node;
  uuid: Scalars['UUID'];
};

export type EdgeInput = {
  nodeInUuid: Scalars['UUID'];
  nodeOutUuid: Scalars['UUID'];
};

export type Graph = {
  __typename?: 'Graph';
  edges: Array<Edge>;
  name: Scalars['String'];
  nodes: Array<Node>;
  uuid: Scalars['UUID'];
};

export type IntFilterLookup = {
  contains?: InputMaybe<Scalars['Int']>;
  endsWith?: InputMaybe<Scalars['Int']>;
  exact?: InputMaybe<Scalars['Int']>;
  gt?: InputMaybe<Scalars['Int']>;
  gte?: InputMaybe<Scalars['Int']>;
  iContains?: InputMaybe<Scalars['Int']>;
  iEndsWith?: InputMaybe<Scalars['Int']>;
  iExact?: InputMaybe<Scalars['Int']>;
  iRegex?: InputMaybe<Scalars['String']>;
  iStartsWith?: InputMaybe<Scalars['Int']>;
  inList?: InputMaybe<Array<Scalars['Int']>>;
  isNull?: InputMaybe<Scalars['Boolean']>;
  lt?: InputMaybe<Scalars['Int']>;
  lte?: InputMaybe<Scalars['Int']>;
  range?: InputMaybe<Array<Scalars['Int']>>;
  regex?: InputMaybe<Scalars['String']>;
  startsWith?: InputMaybe<Scalars['Int']>;
};

export type Mutation = {
  __typename?: 'Mutation';
  addEdge?: Maybe<Scalars['Void']>;
  addNode?: Maybe<Scalars['Void']>;
  addScriptCell: ScriptCell;
  deleteEdge?: Maybe<Scalars['Void']>;
  deleteNode?: Maybe<Scalars['Void']>;
  deleteScriptCell?: Maybe<Scalars['Void']>;
  updateNode?: Maybe<Scalars['Void']>;
  updateScriptCells?: Maybe<Scalars['Void']>;
};


export type MutationAddEdgeArgs = {
  newEdge: EdgeInput;
};


export type MutationAddNodeArgs = {
  newNode: NodeCreate;
};


export type MutationAddScriptCellArgs = {
  newScriptCell: NewScriptCellInput;
  nodeUuid: Scalars['UUID'];
};


export type MutationDeleteEdgeArgs = {
  edgeUuid: Scalars['UUID'];
};


export type MutationDeleteNodeArgs = {
  nodeUuid: Scalars['UUID'];
};


export type MutationDeleteScriptCellArgs = {
  scriptCellUuid: Scalars['UUID'];
};


export type MutationUpdateNodeArgs = {
  nodeUpdate: NodeUpdate;
};


export type MutationUpdateScriptCellsArgs = {
  newCells: Array<ScriptCellInput>;
};

export type NewScriptCellInput = {
  cellCode: Scalars['String'];
  cellOrder?: InputMaybe<Scalars['Int']>;
  cellType?: InputMaybe<CellType>;
};

export type Node = {
  __typename?: 'Node';
  color: Scalars['String'];
  inEdges: Array<Edge>;
  name: Scalars['String'];
  outEdges: Array<Edge>;
  positionX: Scalars['Float'];
  positionY: Scalars['Float'];
  scriptCells: Array<ScriptCell>;
  uuid: Scalars['UUID'];
};

export type NodeCreate = {
  color?: InputMaybe<Scalars['String']>;
  graphUuid: Scalars['UUID'];
  name: Scalars['String'];
  positionX?: InputMaybe<Scalars['Float']>;
  positionY?: InputMaybe<Scalars['Float']>;
};

export type NodeUpdate = {
  color?: InputMaybe<Scalars['String']>;
  name?: InputMaybe<Scalars['String']>;
  positionX?: InputMaybe<Scalars['Float']>;
  positionY?: InputMaybe<Scalars['Float']>;
  uuid: Scalars['UUID'];
};

export type Query = {
  __typename?: 'Query';
  graph: Graph;
  graphs: Array<Graph>;
  node: Node;
  nodes: Array<Node>;
  streamPoint: StreamPoint;
  streamPoints: Array<StreamPoint>;
};


export type QueryGraphArgs = {
  pk: Scalars['ID'];
};


export type QueryNodeArgs = {
  pk: Scalars['ID'];
};


export type QueryStreamPointArgs = {
  pk: Scalars['ID'];
};


export type QueryStreamPointsArgs = {
  filters?: InputMaybe<StreamPointFilter>;
};

export type ScriptCell = {
  __typename?: 'ScriptCell';
  cellCode: Scalars['String'];
  cellOrder: Scalars['Int'];
  cellType: CellType;
  node: Node;
  uuid: Scalars['UUID'];
};

export type ScriptCellInput = {
  cellCode: Scalars['String'];
  cellOrder?: InputMaybe<Scalars['Int']>;
  cellType?: InputMaybe<CellType>;
  uuid?: InputMaybe<Scalars['UUID']>;
};

export type StreamPoint = {
  __typename?: 'StreamPoint';
  createdDate: Scalars['DateTime'];
  host: Scalars['String'];
  janusInPort?: Maybe<Scalars['Int']>;
  janusOutPort?: Maybe<Scalars['Int']>;
  lastLive?: Maybe<Scalars['DateTime']>;
  modifiedDate: Scalars['DateTime'];
  port: Scalars['Int'];
  useInput: Scalars['Boolean'];
  uuid: Scalars['UUID'];
};

export type StreamPointFilter = {
  janusInPort?: InputMaybe<IntFilterLookup>;
  uuid?: InputMaybe<UuidFilterLookup>;
};

export type Subscription = {
  __typename?: 'Subscription';
  count: Scalars['Int'];
  graph: Graph;
  node: Node;
};


export type SubscriptionCountArgs = {
  target?: Scalars['Int'];
};


export type SubscriptionGraphArgs = {
  graphUuid: Scalars['UUID'];
};


export type SubscriptionNodeArgs = {
  nodeUuid: Scalars['UUID'];
};

export type UuidFilterLookup = {
  contains?: InputMaybe<Scalars['UUID']>;
  endsWith?: InputMaybe<Scalars['UUID']>;
  exact?: InputMaybe<Scalars['UUID']>;
  gt?: InputMaybe<Scalars['UUID']>;
  gte?: InputMaybe<Scalars['UUID']>;
  iContains?: InputMaybe<Scalars['UUID']>;
  iEndsWith?: InputMaybe<Scalars['UUID']>;
  iExact?: InputMaybe<Scalars['UUID']>;
  iRegex?: InputMaybe<Scalars['String']>;
  iStartsWith?: InputMaybe<Scalars['UUID']>;
  inList?: InputMaybe<Array<Scalars['UUID']>>;
  isNull?: InputMaybe<Scalars['Boolean']>;
  lt?: InputMaybe<Scalars['UUID']>;
  lte?: InputMaybe<Scalars['UUID']>;
  range?: InputMaybe<Array<Scalars['UUID']>>;
  regex?: InputMaybe<Scalars['String']>;
  startsWith?: InputMaybe<Scalars['UUID']>;
};

export type GetGraphsQueryVariables = Exact<{ [key: string]: never; }>;


export type GetGraphsQuery = { __typename?: 'Query', graphs: Array<{ __typename?: 'Graph', uuid: any, name: string }> };

export type CreateEdgeMutationVariables = Exact<{
  nodeInUuid: Scalars['UUID'];
  nodeOutUuid: Scalars['UUID'];
}>;


export type CreateEdgeMutation = { __typename?: 'Mutation', addEdge?: any | null };

export type CreateNodeMutationVariables = Exact<{
  name: Scalars['String'];
  graphUuid: Scalars['UUID'];
  color?: InputMaybe<Scalars['String']>;
  positionX?: InputMaybe<Scalars['Float']>;
  positionY?: InputMaybe<Scalars['Float']>;
}>;


export type CreateNodeMutation = { __typename?: 'Mutation', addNode?: any | null };

export type UpdateNodeMutationVariables = Exact<{
  nodeUuid: Scalars['UUID'];
  name?: InputMaybe<Scalars['String']>;
  color?: InputMaybe<Scalars['String']>;
  positionX?: InputMaybe<Scalars['Float']>;
  positionY?: InputMaybe<Scalars['Float']>;
}>;


export type UpdateNodeMutation = { __typename?: 'Mutation', updateNode?: any | null };

export type DeleteNodeMutationVariables = Exact<{
  nodeUuid: Scalars['UUID'];
}>;


export type DeleteNodeMutation = { __typename?: 'Mutation', deleteNode?: any | null };

export type DeleteEdgeMutationVariables = Exact<{
  edgeUuid: Scalars['UUID'];
}>;


export type DeleteEdgeMutation = { __typename?: 'Mutation', deleteEdge?: any | null };

export type CreateScriptCellMutationVariables = Exact<{
  nodeUuid: Scalars['UUID'];
  newScriptCell: NewScriptCellInput;
}>;


export type CreateScriptCellMutation = { __typename?: 'Mutation', addScriptCell: { __typename?: 'ScriptCell', cellOrder: number, uuid: any, cellType: CellType, cellCode: string } };

export type DeleteScriptCellMutationVariables = Exact<{
  scriptCellUuid: Scalars['UUID'];
}>;


export type DeleteScriptCellMutation = { __typename?: 'Mutation', deleteScriptCell?: any | null };

export type UpdateScriptCellsMutationVariables = Exact<{
  newCells: Array<ScriptCellInput> | ScriptCellInput;
}>;


export type UpdateScriptCellsMutation = { __typename?: 'Mutation', updateScriptCells?: any | null };

export type CountSubscriptionSubscriptionVariables = Exact<{ [key: string]: never; }>;


export type CountSubscriptionSubscription = { __typename?: 'Subscription', count: number };

export type GraphSubscriptionVariables = Exact<{
  uuid: Scalars['UUID'];
}>;


export type GraphSubscription = { __typename?: 'Subscription', graph: { __typename?: 'Graph', name: string, uuid: any, edges: Array<{ __typename?: 'Edge', uuid: any, outNode: { __typename?: 'Node', uuid: any }, inNode: { __typename?: 'Node', uuid: any } }>, nodes: Array<{ __typename?: 'Node', name: string, uuid: any, positionX: number, positionY: number, color: string, scriptCells: Array<{ __typename?: 'ScriptCell', cellCode: string, cellOrder: number, cellType: CellType, uuid: any }> }> } };

export type NodeSubscriptionVariables = Exact<{
  uuid: Scalars['UUID'];
}>;


export type NodeSubscription = { __typename?: 'Subscription', node: { __typename?: 'Node', color: string, name: string, positionX: number, positionY: number, uuid: any, scriptCells: Array<{ __typename?: 'ScriptCell', cellCode: string, cellOrder: number, cellType: CellType, uuid: any }> } };


export const GetGraphsDocument = gql`
    query GetGraphs {
  graphs {
    uuid
    name
  }
}
    `;

export function useGetGraphsQuery(options: Omit<Urql.UseQueryArgs<never, GetGraphsQueryVariables>, 'query'> = {}) {
  return Urql.useQuery<GetGraphsQuery>({ query: GetGraphsDocument, ...options });
};
export const CreateEdgeDocument = gql`
    mutation createEdge($nodeInUuid: UUID!, $nodeOutUuid: UUID!) {
  addEdge(newEdge: {nodeInUuid: $nodeInUuid, nodeOutUuid: $nodeOutUuid})
}
    `;

export function useCreateEdgeMutation() {
  return Urql.useMutation<CreateEdgeMutation, CreateEdgeMutationVariables>(CreateEdgeDocument);
};
export const CreateNodeDocument = gql`
    mutation createNode($name: String!, $graphUuid: UUID!, $color: String, $positionX: Float, $positionY: Float) {
  addNode(
    newNode: {name: $name, graphUuid: $graphUuid, color: $color, positionX: $positionX, positionY: $positionY}
  )
}
    `;

export function useCreateNodeMutation() {
  return Urql.useMutation<CreateNodeMutation, CreateNodeMutationVariables>(CreateNodeDocument);
};
export const UpdateNodeDocument = gql`
    mutation updateNode($nodeUuid: UUID!, $name: String, $color: String, $positionX: Float, $positionY: Float) {
  updateNode(
    nodeUpdate: {uuid: $nodeUuid, name: $name, color: $color, positionX: $positionX, positionY: $positionY}
  )
}
    `;

export function useUpdateNodeMutation() {
  return Urql.useMutation<UpdateNodeMutation, UpdateNodeMutationVariables>(UpdateNodeDocument);
};
export const DeleteNodeDocument = gql`
    mutation deleteNode($nodeUuid: UUID!) {
  deleteNode(nodeUuid: $nodeUuid)
}
    `;

export function useDeleteNodeMutation() {
  return Urql.useMutation<DeleteNodeMutation, DeleteNodeMutationVariables>(DeleteNodeDocument);
};
export const DeleteEdgeDocument = gql`
    mutation deleteEdge($edgeUuid: UUID!) {
  deleteEdge(edgeUuid: $edgeUuid)
}
    `;

export function useDeleteEdgeMutation() {
  return Urql.useMutation<DeleteEdgeMutation, DeleteEdgeMutationVariables>(DeleteEdgeDocument);
};
export const CreateScriptCellDocument = gql`
    mutation createScriptCell($nodeUuid: UUID!, $newScriptCell: NewScriptCellInput!) {
  addScriptCell(nodeUuid: $nodeUuid, newScriptCell: $newScriptCell) {
    cellOrder
    uuid
    cellType
    cellCode
  }
}
    `;

export function useCreateScriptCellMutation() {
  return Urql.useMutation<CreateScriptCellMutation, CreateScriptCellMutationVariables>(CreateScriptCellDocument);
};
export const DeleteScriptCellDocument = gql`
    mutation deleteScriptCell($scriptCellUuid: UUID!) {
  deleteScriptCell(scriptCellUuid: $scriptCellUuid)
}
    `;

export function useDeleteScriptCellMutation() {
  return Urql.useMutation<DeleteScriptCellMutation, DeleteScriptCellMutationVariables>(DeleteScriptCellDocument);
};
export const UpdateScriptCellsDocument = gql`
    mutation updateScriptCells($newCells: [ScriptCellInput!]!) {
  updateScriptCells(newCells: $newCells)
}
    `;

export function useUpdateScriptCellsMutation() {
  return Urql.useMutation<UpdateScriptCellsMutation, UpdateScriptCellsMutationVariables>(UpdateScriptCellsDocument);
};
export const CountSubscriptionDocument = gql`
    subscription CountSubscription {
  count
}
    `;

export function useCountSubscriptionSubscription<R = CountSubscriptionSubscription>(options: Omit<Urql.UseSubscriptionArgs<never, CountSubscriptionSubscriptionVariables>, 'query'> = {}, handler?: Urql.SubscriptionHandlerArg<CountSubscriptionSubscription, R>) {
  return Urql.useSubscription<CountSubscriptionSubscription, R, CountSubscriptionSubscriptionVariables>({ query: CountSubscriptionDocument, ...options }, handler);
};
export const GraphDocument = gql`
    subscription graph($uuid: UUID!) {
  graph(graphUuid: $uuid) {
    name
    uuid
    edges {
      uuid
      outNode {
        uuid
      }
      inNode {
        uuid
      }
    }
    nodes {
      name
      uuid
      scriptCells {
        cellCode
        cellOrder
        cellType
        uuid
      }
      positionX
      positionY
      color
    }
  }
}
    `;

export function useGraphSubscription<R = GraphSubscription>(options: Omit<Urql.UseSubscriptionArgs<never, GraphSubscriptionVariables>, 'query'> = {}, handler?: Urql.SubscriptionHandlerArg<GraphSubscription, R>) {
  return Urql.useSubscription<GraphSubscription, R, GraphSubscriptionVariables>({ query: GraphDocument, ...options }, handler);
};
export const NodeDocument = gql`
    subscription node($uuid: UUID!) {
  node(nodeUuid: $uuid) {
    color
    name
    positionX
    positionY
    scriptCells {
      cellCode
      cellOrder
      cellType
      uuid
    }
    uuid
  }
}
    `;

export function useNodeSubscription<R = NodeSubscription>(options: Omit<Urql.UseSubscriptionArgs<never, NodeSubscriptionVariables>, 'query'> = {}, handler?: Urql.SubscriptionHandlerArg<NodeSubscription, R>) {
  return Urql.useSubscription<NodeSubscription, R, NodeSubscriptionVariables>({ query: NodeDocument, ...options }, handler);
};
