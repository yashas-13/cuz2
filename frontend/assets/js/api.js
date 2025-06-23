const API_BASE = (typeof window !== 'undefined' && window.API_BASE !== undefined)
  ? window.API_BASE
  : 'http://localhost:5000';

async function apiFetch(url, options = {}) {
  const token = localStorage.getItem('token');
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const resp = await fetch(API_BASE + url, { ...options, headers });
  if (resp.status === 401) {
    localStorage.removeItem('token');
  }
  return resp;
}
if (typeof module !== 'undefined') {
  module.exports = { apiFetch };
}
if (typeof window !== 'undefined') {
  window.apiFetch = apiFetch;
}

export { apiFetch };
