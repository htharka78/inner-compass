const CACHE = 'compass-v6';
const ASSETS = ['./', './index.html', './manifest.json', './icon.png', './icon.svg'];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => k !== CACHE).map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request))
  );
});

// Tap a notification → open / focus the app
self.addEventListener('notificationclick', e => {
  e.notification.close();
  const tab = e.notification.data?.tab || 'today';
  e.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then(list => {
        for (const client of list) {
          if ('focus' in client) {
            client.postMessage({ type: 'OPEN_TAB', tab });
            return client.focus();
          }
        }
        return self.clients.openWindow('./?tab=' + tab);
      })
  );
});

// Page sends scheduled notification requests → SW shows them
// (fires even when page is backgrounded, as long as SW is active)
self.addEventListener('message', e => {
  if (e.data?.type === 'SHOW_NOTIF') {
    const { title, body, tag, tab } = e.data;
    self.registration.showNotification(title, {
      body,
      icon: './icon.png',
      badge: './icon.png',
      tag,
      renotify: false,
      data: { tab }
    });
  }
});
