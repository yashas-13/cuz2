import { queueRequest } from './offline.js';

async function createRequest() {
  const req = { url: '/requests/', options: { method: 'POST', body: JSON.stringify({product_id:1, action:'ship'}), headers: {} } };
  if (navigator.onLine) {
    await window.apiFetch(req.url, req.options);
  } else {
    await queueRequest(req);
    document.body.classList.add('offline');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.body.addEventListener('click', createRequest);
});
