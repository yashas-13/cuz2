import { queueRequest } from './offline.js';

async function loadProducts() {
  const resp = await window.apiFetch('/products/');
  const data = await resp.json();
  console.log(data);
}

export async function bulkApprove(ids) {
  await window.apiFetch('/requests/bulk-approve', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ids })
  });
}

export async function bulkDeny(ids) {
  await window.apiFetch('/requests/bulk-deny', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ids })
  });
}

export async function uploadProducts(list) {
  await window.apiFetch('/products/bulk', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(list)
  });
}

export async function updateProducts(list) {
  await window.apiFetch('/products/bulk', {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(list)
  });
}

async function loadAnalytics() {
  const ctx = document.getElementById('salesChart');
  if (!ctx) return;
  const resp = await window.apiFetch('/analytics/sales');
  const data = await resp.json();
  window.renderSalesChart(ctx, data);
}

window.addEventListener('load', () => {
  loadProducts();
  loadAnalytics();
});
