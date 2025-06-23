import { apiFetch } from './api.js';

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('loginForm');
  if (!form) return;
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const resp = await apiFetch('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    });
    if (resp.ok) {
      const data = await resp.json();
      localStorage.setItem('token', data.access_token);
      try {
        const payload = JSON.parse(atob(data.access_token.split('.')[1]));
        const role = payload.role;
        if (role === 'Manufacturer') {
          window.location.href = 'manufacturer.html';
        } else if (role === 'CFA') {
          window.location.href = 'cfa.html';
        } else if (role === 'Stockist') {
          window.location.href = 'stockist.html';
        } else {
          alert('Unknown role');
        }
      } catch (err) {
        console.error(err);
        alert('Invalid token');
      }
    } else {
      alert('Invalid credentials');
    }
  });
});
