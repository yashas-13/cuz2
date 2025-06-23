
async function loadCatalog() {
  const resp = await window.apiFetch('/products/');
  const data = await resp.json();
  console.log('catalog', data);
}

export function getCart() {
  return JSON.parse(localStorage.getItem('cart') || '[]');
}

export function saveCart(cart) {
  localStorage.setItem('cart', JSON.stringify(cart));
}

export function addToCart(item) {
  const cart = getCart();
  const existing = cart.find(i => i.product_id === item.product_id);
  if (existing) existing.qty += item.qty; else cart.push(item);
  saveCart(cart);
}

export function removeFromCart(product_id) {
  const cart = getCart().filter(i => i.product_id !== product_id);
  saveCart(cart);
}

export async function checkout() {
  const cart = getCart();
  await window.apiFetch('/orders/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ items: cart })
  });
  saveCart([]);
}

export async function updateProfile(data) {
  await window.apiFetch('/users/me', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
}

window.addEventListener('load', loadCatalog);

if (typeof module !== 'undefined') {
  module.exports = { getCart, saveCart, addToCart, removeFromCart };
}
