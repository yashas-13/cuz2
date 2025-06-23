import { jest } from '@jest/globals';

let apiFetch;

beforeAll(async () => {
  global.fetch = jest.fn(() => Promise.resolve({ status: 200 }));
  global.window.API_BASE = '';
  localStorage.setItem('token', 'abc');
  ({ apiFetch } = await import('../assets/js/api.js'));
});

test('apiFetch adds auth header', async () => {
  await apiFetch('/');
  expect(fetch).toHaveBeenCalledWith(
    '/',
    expect.objectContaining({
      headers: expect.objectContaining({ Authorization: 'Bearer abc' })
    })
  );
});
