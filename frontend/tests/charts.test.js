let renderSalesChart;
beforeAll(async () => {
  ({ renderSalesChart } = await import('../charts/analytics.js'));
  HTMLCanvasElement.prototype.getContext = () => ({});
});

test('renderSalesChart initializes Chart', () => {
  document.body.innerHTML = '<canvas id="c"></canvas>';
  const ctx = document.getElementById('c');
  const chart = renderSalesChart(ctx, { labels: ['A'], values: [1] });
  expect(chart).toBeDefined();
  chart.destroy();
});
