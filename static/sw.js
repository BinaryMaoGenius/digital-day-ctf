const CACHE_NAME = 'ctf-safari-v1';
const ASSETS_TO_CACHE = [
  '/static/css/modern-ctf.css',
  '/static/js/libs/terminal.min.js',
  '/static/images/pwa-icon-192.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});

// Real-time notification handler (future use)
self.addEventListener('push', (event) => {
  const data = event.data.json();
  const options = {
    body: data.body,
    icon: '/static/images/pwa-icon-192.png',
    badge: '/static/images/pwa-icon-192.png',
    vibrate: [200, 100, 200]
  };
  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});
