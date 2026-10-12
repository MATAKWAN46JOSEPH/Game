const SHELL_CACHE = 'maison-maudite-shell-v1';
const ENGINE_CACHE = 'maison-maudite-engine-v1';
const ENGINE_URL = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
const SHELL_FILES = [
  './index.html',
  './manifest.webmanifest',
  './icon.svg',
  './icon-180.png',
  './icon-192.png',
  './icon-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const shell = await caches.open(SHELL_CACHE);
    await shell.addAll(SHELL_FILES);
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 12000);
      const response = await fetch(ENGINE_URL, {
        mode: 'no-cors',
        cache: 'reload',
        signal: controller.signal
      });
      clearTimeout(timeout);
      await (await caches.open(ENGINE_CACHE)).put(ENGINE_URL, response);
    } catch (error) {
      // The game can still be installed; the engine will be fetched on first play.
    }
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keep = new Set([SHELL_CACHE, ENGINE_CACHE]);
    const keys = await caches.keys();
    await Promise.all(keys.filter(key => key.startsWith('maison-maudite-') && !keep.has(key))
      .map(key => caches.delete(key)));
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', event => {
  const request = event.request;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);
  if (url.href === ENGINE_URL) {
    event.respondWith((async () => {
      const cached = await (await caches.open(ENGINE_CACHE)).match(ENGINE_URL);
      if (cached) return cached;
      const response = await fetch(request);
      if (response.ok || response.type === 'opaque') {
        await (await caches.open(ENGINE_CACHE)).put(ENGINE_URL, response.clone());
      }
      return response;
    })());
    return;
  }

  if (url.origin !== self.location.origin) return;
  if (request.mode === 'navigate') {
    event.respondWith(fetch(request).catch(() => caches.match('./index.html')));
    return;
  }
  event.respondWith(caches.match(request).then(cached => cached || fetch(request)));
});
