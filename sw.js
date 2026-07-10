const CACHE_NAME = 'treninkovy-denik-v1';
const ASSETS = [
    './',
    './index.html',
    './manifest.json'
];

// Instalace - uložení souborů do mezipaměti
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            return cache.addAll(ASSETS);
        })
    );
});

// Záchyt požadavků - servírování z mezipaměti, když není internet
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            // Pokud je soubor v cache, vrať ho. Jinak zkus internet.
            return response || fetch(event.request);
        })
    );
});
