const { apiFetch } = require('../assets/js/api.js');
global.fetch = jest.fn(() => Promise.resolve({ status: 200 }));
localStorage.setItem('token', 'abc');

test('apiFetch adds auth header', async () => {
  await apiFetch('/');
  expect(fetch).toHaveBeenCalledWith('/', expect.objectContaining({ headers: expect.objectContaining({ Authorization: 'Bearer abc' }) }));
});
