import type { CodegenConfig } from "@graphql-codegen/cli";

const config: CodegenConfig = {
  generates: {
    "src/graphql.ts": {
      plugins: [
        "typescript",
        "typescript-operations",
        "typescript-vue-urql"
      ],
      documents: "../caster-back/operations.gql",
      overwrite: true,
      schema: "../caster-back/schema.gql",
      config: {
        skipTypename: true
      }
    }
  }
};
export default config;
