async function apiFetch(url, options = {}) {
  const token = localStorage.getItem('token');
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const resp = await fetch(url, { ...options, headers });
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
