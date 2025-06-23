import { queueRequest } from './offline.js';

async function loadProducts() {
  const resp = await window.apiFetch('/products/');
  const data = await resp.json();
  console.log(data);
}

window.addEventListener('load', loadProducts);
