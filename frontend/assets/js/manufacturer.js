import { queueRequest } from './offline.js';

async function loadProducts() {
  const resp = await window.apiFetch('/products/');
  const data = await resp.json();
  console.log(data);
}

async function loadRequests() {
  const resp = await window.apiFetch('/requests?status=pending');
  const data = await resp.json();
  const list = document.getElementById('requestsList');
  if (!list) return;
  list.innerHTML = '';
  data.forEach(r => {
    const li = document.createElement('li');
    li.innerHTML = `<label><input type="checkbox" class="req-check" value="${r.id}">Request ${r.id} (${r.action} ${r.quantity})</label>`;
    list.appendChild(li);
  });
}

function getSelectedIds() {
  return Array.from(document.querySelectorAll('.req-check:checked')).map(c => parseInt(c.value));
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
  loadRequests();
  const approveBtn = document.getElementById('approveSelected');
  const denyBtn = document.getElementById('denySelected');
  if (approveBtn) {
    approveBtn.addEventListener('click', async () => {
      const ids = getSelectedIds();
      if (ids.length) {
        await bulkApprove(ids);
        loadRequests();
      }
    });
  }
  if (denyBtn) {
    denyBtn.addEventListener('click', async () => {
      const ids = getSelectedIds();
      if (ids.length) {
        await bulkDeny(ids);
        loadRequests();
      }
    });
  }
});
