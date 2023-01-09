import { createClient } from "@urql/vue";

export const useUrql = createClient({
  url: "http://someurl.com"
});
