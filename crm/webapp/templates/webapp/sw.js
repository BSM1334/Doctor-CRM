const CACHE_NAME = 'doc-crm-cache-v1';
const ASSETS = [
  '/static/css/style.css',
  '/static/js/app.js',
  '/static/images/doctor_logo.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      // Cache assets
      return cache.addAll(ASSETS).catch(err => {
        console.warn('Failed to pre-cache some assets:', err);
      });
    })
  );
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    fetch(event.request)
      .then(networkResponse => {
        const url = new URL(event.request.url);
        // Only cache our static assets
        if (ASSETS.some(asset => url.pathname.endsWith(asset) || asset.endsWith(url.pathname))) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      })
      .catch(() => {
        return caches.match(event.request).then(response => {
          if (response) {
            return response;
          }
          // fallback if offline
        });
      })
  );
});
