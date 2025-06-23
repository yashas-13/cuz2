import { jest } from '@jest/globals';

let apiFetch;

beforeAll(async () => {
  global.window = { API_BASE: '' };
  global.localStorage = {
    getItem: jest.fn(() => 'abc'),
    setItem: jest.fn(),
    removeItem: jest.fn()
  };
  global.window.localStorage = global.localStorage;
  global.fetch = jest.fn(() => Promise.resolve({ status: 200 }));
  ({ apiFetch } = await import('../assets/js/api.js'));
});

test('apiFetch adds auth header', async () => {
  await apiFetch('/');
  expect(fetch).toHaveBeenCalled();
});
