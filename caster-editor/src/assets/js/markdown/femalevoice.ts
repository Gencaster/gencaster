const FemaleVoice = () => {
  return {
    markdownCommands: {
      // https://discuss.prosemirror.net/t/command-insert-characters-around-selection/2252/2
      // myCommand: (payload, state, dispatch) => {
      myCommand: (payload?, state, dispatch) => {
        const { from, to } = state.selection;
        const { tr } = state;

        const beforeToken = "{speaker[female]}`";
        const afterToken = "`";

        tr.insertText(afterToken, to);
        tr.insertText(beforeToken, from);
        dispatch(tr);

        return true;
      }
    }
    // wysiwygCommands: {
    //   myCommand: (payload, state, dispatch) => {
    //     // ...
    //     return true;
    //   }
    // }
  };
};
export default FemaleVoice;
