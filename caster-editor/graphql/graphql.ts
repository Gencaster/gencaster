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
};

export type Edge = {
  __typename?: 'Edge';
  inNode: Node;
  outNode: Node;
  uuid: Scalars['UUID'];
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

export type Node = {
  __typename?: 'Node';
  inEdges: Array<Edge>;
  name: Scalars['String'];
  outEdges: Array<Edge>;
  scriptCells: Array<ScriptCell>;
  uuid: Scalars['UUID'];
};

export type Query = {
  __typename?: 'Query';
  graphs: Array<Graph>;
  streamPoint: StreamPoint;
  streamPoints: Array<StreamPoint>;
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
