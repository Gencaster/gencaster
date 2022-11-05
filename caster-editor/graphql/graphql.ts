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
  deleteEdge?: Maybe<Scalars['Void']>;
  deleteNode?: Maybe<Scalars['Void']>;
};


export type MutationAddEdgeArgs = {
  newEdge: EdgeInput;
};


export type MutationAddNodeArgs = {
  newNode: NodeInput;
};


export type MutationDeleteEdgeArgs = {
  edgeUuid: Scalars['UUID'];
};


export type MutationDeleteNodeArgs = {
  nodeUuid: Scalars['UUID'];
};

export type Node = {
  __typename?: 'Node';
  inEdges: Array<Edge>;
  name: Scalars['String'];
  outEdges: Array<Edge>;
  scriptCells: Array<ScriptCell>;
  uuid: Scalars['UUID'];
};

export type NodeInput = {
  graphUuid: Scalars['UUID'];
  name: Scalars['String'];
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
  pk?: InputMaybe<Scalars['ID']>;
};


export type QueryNodeArgs = {
  pk?: InputMaybe<Scalars['ID']>;
};


export type QueryStreamPointArgs = {
  pk?: InputMaybe<Scalars['ID']>;
};


export type QueryStreamPointsArgs = {
  filters?: InputMaybe<StreamPointFilter>;
};

export type ScriptCell = {
  __typename?: 'ScriptCell';
  cellCode: Scalars['String'];
  cellOrder: Scalars['Int'];
  cellType: Scalars['String'];
  node: Node;
  uuid: Scalars['UUID'];
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
};


export type SubscriptionCountArgs = {
  target?: Scalars['Int'];
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

export type MyQueryQueryVariables = Exact<{ [key: string]: never; }>;


export type MyQueryQuery = { __typename?: 'Query', graphs: Array<{ __typename?: 'Graph', name: string }> };

export type TestQueryQueryVariables = Exact<{ [key: string]: never; }>;


export type TestQueryQuery = { __typename?: 'Query', graphs: Array<{ __typename?: 'Graph', name: string, nodes: Array<{ __typename?: 'Node', name: string }>, edges: Array<{ __typename?: 'Edge', uuid: any }> }> };

export type GetGraphsQueryVariables = Exact<{ [key: string]: never; }>;


export type GetGraphsQuery = { __typename?: 'Query', graphs: Array<{ __typename?: 'Graph', uuid: any, name: string }> };

export type GetGraphQueryVariables = Exact<{
  uuid?: InputMaybe<Scalars['ID']>;
}>;


export type GetGraphQuery = { __typename?: 'Query', graph: { __typename?: 'Graph', name: string, uuid: any, edges: Array<{ __typename?: 'Edge', uuid: any, outNode: { __typename?: 'Node', uuid: any }, inNode: { __typename?: 'Node', uuid: any } }>, nodes: Array<{ __typename?: 'Node', name: string, uuid: any, scriptCells: Array<{ __typename?: 'ScriptCell', cellCode: string, cellOrder: number, cellType: string, uuid: any }> }> } };

export type CreateEdgeMutationVariables = Exact<{
  nodeInUuid: Scalars['UUID'];
  nodeOutUuid: Scalars['UUID'];
}>;


export type CreateEdgeMutation = { __typename?: 'Mutation', addEdge?: any | null };

export type CreateNodeMutationVariables = Exact<{
  name: Scalars['String'];
  graphUuid: Scalars['UUID'];
}>;


export type CreateNodeMutation = { __typename?: 'Mutation', addNode?: any | null };

export type DeleteNodeMutationVariables = Exact<{
  nodeUuid: Scalars['UUID'];
}>;


export type DeleteNodeMutation = { __typename?: 'Mutation', deleteNode?: any | null };

export type DeleteEdgeMutationVariables = Exact<{
  edgeUuid: Scalars['UUID'];
}>;


export type DeleteEdgeMutation = { __typename?: 'Mutation', deleteEdge?: any | null };


export const MyQueryDocument = gql`
    query MyQuery {
  graphs {
    name
  }
}
    `;

export function useMyQueryQuery(options: Omit<Urql.UseQueryArgs<never, MyQueryQueryVariables>, 'query'> = {}) {
  return Urql.useQuery<MyQueryQuery>({ query: MyQueryDocument, ...options });
};
export const TestQueryDocument = gql`
    query testQuery {
  graphs {
    nodes {
      name
    }
    edges {
      uuid
    }
    name
  }
}
    `;

export function useTestQueryQuery(options: Omit<Urql.UseQueryArgs<never, TestQueryQueryVariables>, 'query'> = {}) {
  return Urql.useQuery<TestQueryQuery>({ query: TestQueryDocument, ...options });
};
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
export const GetGraphDocument = gql`
    query getGraph($uuid: ID) {
  graph(pk: $uuid) {
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
    }
  }
}
    `;

export function useGetGraphQuery(options: Omit<Urql.UseQueryArgs<never, GetGraphQueryVariables>, 'query'> = {}) {
  return Urql.useQuery<GetGraphQuery>({ query: GetGraphDocument, ...options });
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
    mutation createNode($name: String!, $graphUuid: UUID!) {
  addNode(newNode: {name: $name, graphUuid: $graphUuid})
}
    `;

export function useCreateNodeMutation() {
  return Urql.useMutation<CreateNodeMutation, CreateNodeMutationVariables>(CreateNodeDocument);
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
