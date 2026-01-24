document.addEventListener("DOMContentLoaded", () => {
  const ctx = document.getElementById("graficoLinha");
  if (!ctx || !window.graficoLabels) return;

  new Chart(ctx, {
    type: "line",
    data: {
      labels: window.graficoLabels,
      datasets: [{
        data: window.graficoValores,
        borderColor: "#3b82f6",
        backgroundColor: "rgba(59,130,246,.15)",
        tension: 0.4,
        fill: true
      }]
    },
    options: {
      plugins: { legend: { display: false } }
    }
  });
});
