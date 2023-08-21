import type { CompletionContext } from "@codemirror/autocomplete";

const completePython = (context: CompletionContext) => {
  const word = context.matchBefore(/\w*/);
  if (word?.from == word?.to && !context.explicit) return null;
  return {
    from: word?.from,
    options: [
      { label: "match", type: "keyword" },
      { label: "hello", type: "variable", info: "(World)" },
      { label: "magic", type: "text", apply: "⠁⭒*.✩.*⭒⠁", detail: "macro" },
    ],
  };
};

export default completePython;
