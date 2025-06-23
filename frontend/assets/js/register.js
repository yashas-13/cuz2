async function register(e) {
  e.preventDefault();
  const data = {
    username: document.getElementById('username').value,
    email: document.getElementById('email').value,
    password: document.getElementById('password').value
  };
  const resp = await window.apiFetch('/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (resp.ok) {
    alert('Registered');
  } else {
    const t = await resp.json();
    alert(t.msg || 'error');
  }
}

document.getElementById('regForm').addEventListener('submit', register);
