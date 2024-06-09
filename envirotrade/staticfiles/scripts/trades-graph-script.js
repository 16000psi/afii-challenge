class TradesGraphScript {
  constructor(node) {
    this.tradesGraph = node;
    this.fetchDomData();
    this.addEventListeners();
    this.fetchAllData();
  }

  fetchDomData() {
    this.chartTitle = this.tradesGraph.querySelector("#chart-title");
    this.priceChartTitle = this.tradesGraph.querySelector("#price-chart-title");
    this.daysAgoSelector = this.tradesGraph.querySelector("#days_ago_selector");
    this.parameterSelector = this.tradesGraph.querySelector(
      "#parameter_selector",
    );
    this.metricSelector = this.tradesGraph.querySelector("#metric_selector");
    this.instrumentTypeSelector = this.tradesGraph.querySelector(
      "#instrument_type_selector",
    );
  }

  addEventListeners() {
    this.daysAgoSelector.addEventListener("change", () => {
      this.fetchAllData();
    });
    this.metricSelector.addEventListener("change", () => {
      this.fetchPriceData();
    });
    this.parameterSelector.addEventListener("change", () => {
      this.fetchTradeData();
    });
    this.instrumentTypeSelector.addEventListener("change", () => {
      this.updateMetricOptions();
      this.fetchPriceData();
    });
  }

  fetchAllData() {
    this.fetchTradeData();
    this.fetchPriceData();
  }

  fetchTradeData() {
    const daysAgo = this.daysAgoSelector.value;
    const parameter = this.parameterSelector.value;

    this.updateChartTitle(parameter);

    fetch(`/trade_counts/${daysAgo}/${parameter}/`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((tradeData) => {
        this.updateChart(tradeData, parameter);
      })
      .catch((error) => {
        console.error("Error fetching trade data:", error);
      });
  }

  updateChartTitle(parameter) {
    if (parameter === "strategy") {
      this.chartTitle.textContent = "Trades by Strategy";
    } else {
      this.chartTitle.textContent = "Trades by Instrument Type";
    }
  }

  updateChart(tradeData, parameter) {
    const labels = tradeData.map((trade) => trade[parameter]);
    const data = tradeData.map((trade) => trade.count);

    const ctx = this.tradesGraph
      .querySelector("#graph-container")
      .getContext("2d");
    if (window.tradeChart) {
      window.tradeChart.data.labels = labels;
      window.tradeChart.data.datasets[0].data = data;
      window.tradeChart.update();
    } else {
      window.tradeChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Number of Trades",
              data: data,
              backgroundColor: "#3beccd",
              borderColor: "#3beccd",
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              labels: {
                color: "#dce0d9",
              },
              onClick: null,
            },
            title: {
              display: false,
            },
          },
          scales: {
            x: {
              ticks: {
                color: "#dce0d9",
              },
            },
            y: {
              beginAtZero: true,
              ticks: {
                color: "#dce0d9",
              },
            },
          },
        },
      });
    }
  }

  fetchPriceData() {
    const instrumentType = this.instrumentTypeSelector.value;
    const metric = this.metricSelector.value;
    const daysAgo = this.daysAgoSelector.value;

    fetch(`/type_chart/${daysAgo}/${instrumentType}/${metric}/`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((priceData) => {
        this.updatePriceChart(priceData);
        this.updatePriceChartTitle(instrumentType, metric);
      })
      .catch((error) => {
        console.error("Error fetching price data:", error);
      });
  }

  updatePriceChartTitle(instrumentType, metric) {
    let styledMetric = "Price";
    let styledInstrumentType = "Bonds";

    if (metric === "spread") {
      styledMetric = "Spread";
    } else if (metric === "notional") {
      styledMetric = "Notional";
    } else if (metric === "no_of_contracts") {
      styledMetric = "No. of Contracts";
    }

    if (instrumentType === "futures") {
      styledInstrumentType = "Futures";
    } else if (instrumentType === "cds") {
      styledInstrumentType = "CDS";
    } else if (instrumentType === "fx") {
      styledInstrumentType = "FX";
    }

    this.priceChartTitle.textContent = `${styledMetric} for ${styledInstrumentType}`;
  }

  updatePriceChart(priceData) {
    const labels = priceData.map((data) => data.price_bin);
    const data = priceData.map((data) => data.count);

    const ctx = this.tradesGraph
      .querySelector("#price-graph-container")
      .getContext("2d");
    if (window.priceChart) {
      window.priceChart.data.labels = labels;
      window.priceChart.data.datasets[0].data = data;
      window.priceChart.update();
    } else {
      window.priceChart = new Chart(ctx, {
        type: "line",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Number of Trades Spread",
              data: data,
              backgroundColor: "rgba(59, 236, 205, 0.2)",
              borderColor: "#fd5765",
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              labels: {
                color: "#dce0d9",
              },
              onClick: null,
            },
            title: {
              display: false,
            },
          },
          scales: {
            x: {
              ticks: {
                color: "#dce0d9",
              },
            },
            y: {
              beginAtZero: true,
              ticks: {
                color: "#dce0d9",
              },
            },
          },
        },
      });
    }
  }

  updateMetricOptions() {
    const instrumentType = this.instrumentTypeSelector.value;
    const metricOptions = {
      bond: [
        { value: "price", text: "Price" },
        { value: "spread", text: "Spread" },
        { value: "notional", text: "Notional" },
      ],
      cds: [
        { value: "spread", text: "Spread" },
        { value: "notional", text: "Notional" },
      ],
      futures: [
        { value: "price", text: "Price" },
        { value: "no_of_contracts", text: "No. of Contracts" },
      ],
      fx: [
        { value: "price", text: "Price" },
        { value: "notional", text: "Notional" },
      ],
    };

    while (this.metricSelector.options.length > 0) {
      this.metricSelector.remove(0);
    }

    const options = metricOptions[instrumentType];
    options.forEach((option) => {
      const newOption = document.createElement("option");
      newOption.value = option.value;
      newOption.textContent = option.text;
      this.metricSelector.appendChild(newOption);
    });
  }
}

export default TradesGraphScript;
