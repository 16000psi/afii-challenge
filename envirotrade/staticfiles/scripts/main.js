import NewTradeFormScript from "./new-trade-form-script.js";
import TradesGraphScript from "./trades-graph-script.js";

document.addEventListener("DOMContentLoaded", () => {
  const newTradeForms = document.querySelectorAll("div[data-new-trade-form]");
  newTradeForms.forEach((newTradeForm) => {
    new NewTradeFormScript(newTradeForm);
  });
  const graphDisplays = document.querySelectorAll("div[data-graph-display]");
  graphDisplays.forEach((graphDisplay) => {
    new TradesGraphScript(graphDisplay);
  });

});
