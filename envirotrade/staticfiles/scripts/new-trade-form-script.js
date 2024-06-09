class NewTradeFormScript {
  constructor(node) {
    this.newTradeForm = node;
    this.getDomData();
    this.strategyOptions = {
      bond: [
        { value: "active_short", text: "Active Short" },
        { value: "relval", text: "Relval" },
        { value: "slbs", text: "SLBS" },
        { value: "curves", text: "Curves" },
        { value: "use_of_proceeds", text: "Use of Proceeds" },
        { value: "", text: "--" },
      ],
      cds: [
        { value: "active_short", text: "Active Short" },
        { value: "relval", text: "Relval" },
        { value: "slbs", text: "SLBS" },
        { value: "curves", text: "Curves" },
        { value: "use_of_proceeds", text: "Use of Proceeds" },
        { value: "", text: "--" },
      ],
      futures: [
        { value: "hedge", text: "Hedge" },
        { value: "", text: "--" },
      ],
      fx: [
        { value: "hedge", text: "Hedge" },
        { value: "", text: "--" },
      ],
    };

    this.radioButtons.forEach((radio) => {
      radio.addEventListener("change", (event) => {
        this.showFieldsForTradeType(event.target.value);
      });
    });

    this.hideAllFields();
    this.showFieldsForTradeType("bond");
  }

  getDomData() {
    this.radioButtons = this.newTradeForm.querySelectorAll('input[name="trade_type"]');
    this.formGroups = {
      price: this.newTradeForm.querySelectorAll('[data-field="price"]'),
      spread: this.newTradeForm.querySelectorAll('[data-field="spread"]'),
      notional: this.newTradeForm.querySelectorAll('[data-field="notional"]'),
      direction: this.newTradeForm.querySelectorAll('[data-field="direction"]'),
      no_of_contracts: this.newTradeForm.querySelectorAll('[data-field="no_of_contracts"]'),
    };

    this.strategyGroup = this.newTradeForm.querySelector('[data-field="strategy"]');
    this.strategySelect = this.strategyGroup.querySelector("select");
    this.tradeTypeInput = this.newTradeForm.querySelector("#trade_type");
  }

  updateStrategyOptions = (tradeType) => {
    this.strategySelect.innerHTML = "";
    this.strategyOptions[tradeType].forEach((option) => {
      const opt = document.createElement("option");
      opt.value = option.value;
      opt.textContent = option.text;
      this.strategySelect.appendChild(opt);
    });
  };

  hideAllFields = () => {
    for (let key in this.formGroups) {
      this.formGroups[key].forEach((field) => {
        field.style.display = "none";
        field.querySelector("input, select, textarea").removeAttribute("required");
      });
    }
  };

  showFieldsForTradeType = (tradeType) => {
    this.hideAllFields();
    this.tradeTypeInput.value = tradeType;
    switch (tradeType) {
      case "bond":
        this.showFields(['price', 'spread', 'notional', 'direction']);
        break;
      case "cds":
        this.showFields(['spread', 'notional', 'direction']);
        break;
      case "futures":
        this.showFields(['price', 'direction', 'no_of_contracts']);
        break;
      case "fx":
        this.showFields(['price', 'notional', 'direction']);
        break;
    }
    this.updateStrategyOptions(tradeType);
  };

  showFields = (fields) => {
    fields.forEach(field => {
      this.formGroups[field].forEach((fieldElement) => {
        fieldElement.style.display = "block";
        fieldElement.querySelector("input, select, textarea").setAttribute("required", "required");
      });
    });
  };
}

export default NewTradeFormScript;
