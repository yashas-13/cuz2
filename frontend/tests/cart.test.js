let mod;
beforeAll(async () => {
  mod = await import('../assets/js/stockist.js');
});

test('addToCart stores item', () => {
  localStorage.clear();
  mod.addToCart({ product_id: 1, qty: 2 });
  expect(mod.getCart()).toEqual([{ product_id: 1, qty: 2 }]);
});

test('removeFromCart removes item', () => {
  mod.saveCart([{ product_id: 1, qty: 2 }]);
  mod.removeFromCart(1);
  expect(mod.getCart()).toEqual([]);
});
