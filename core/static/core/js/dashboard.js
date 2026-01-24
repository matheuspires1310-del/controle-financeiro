document.addEventListener("DOMContentLoaded", () => {
  const ctx = document.getElementById("graficoLinha");
  if (!ctx) return;

  new Chart(ctx, {
    type: "line",
    data: {
      labels: window.graficoLabels,
      datasets: [{
          data: window.graficoValores,

        borderColor: "#3b82f6",
        backgroundColor: "rgba(59,130,246,.15)",
        tension: 0.45,
        fill: true,
        pointRadius: 4,
        pointBackgroundColor: "#3b82f6"
      }]
    },
    options: {
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: {
          ticks: { color: "#94a3b8" },
          grid: { color: "rgba(255,255,255,.05)" }
        },
        y: {
          ticks: { color: "#94a3b8" },
          grid: { color: "rgba(255,255,255,.08)" }
        }
      }
    }
  });
});
