
async function loadCatalog() {
  const resp = await window.apiFetch('/products/');
  const data = await resp.json();
  console.log('catalog', data);
}

window.addEventListener('load', loadCatalog);
