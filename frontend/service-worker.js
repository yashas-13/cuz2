self.addEventListener('install', event => {
  event.waitUntil(caches.open('scm-v1').then(cache => cache.addAll([
    '/',
    '/assets/css/style.css'
  ])));
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(resp => resp || fetch(event.request))
  );
});
