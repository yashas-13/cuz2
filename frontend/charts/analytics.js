import Chart from 'chart.js/auto';

export function renderSalesChart(ctx, data) {
  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.labels,
      datasets: [{ label: 'Sales', data: data.values }]
    }
  });
}

if (typeof window !== 'undefined') {
  window.renderSalesChart = renderSalesChart;
}
if (typeof module !== 'undefined') {
  module.exports = { renderSalesChart };
}
