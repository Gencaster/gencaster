import type { CompletionContext } from "@codemirror/autocomplete";
import engineVars from "@/engineVars.json";

const completePython = (context: CompletionContext) => {
  const word = context.matchBefore(/\w*/);
  if (word?.from == word?.to && !context.explicit) return null;
  return {
    from: word?.from,
    options: engineVars,
  };
};

export default completePython;
