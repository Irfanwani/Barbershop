const staticCacheName = 'site-static-v2';
//const dynamicCache = 'dynamic-cache-v1';
const assets = [
    '/static/images/head_icon.png',
    '/static/images/icon.png',
    "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css",
    "https://pro.fontawesome.com/releases/v5.10.0/css/all.css",
    "https://code.jquery.com/jquery-3.5.1.min.js",
    "https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.23.0/moment.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/tempusdominus-bootstrap-4/5.1.2/css/tempusdominus-bootstrap-4.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/tempusdominus-bootstrap-4/5.1.2/js/tempusdominus-bootstrap-4.min.js",
    "https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js",
    "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js",
    '/static/snake-game.html'
];

// installation event
self.addEventListener('install', evt => {
    console.log('Service worker has been installed.');
    evt.waitUntil(
        caches.open(staticCacheName).then(cache => {
            console.log('caching site assets');
            cache.addAll(assets);
        })
    )
});

// activation event
self.addEventListener('activate', evt => {
    //console.log('Service worker has been activated.');
    evt.waitUntil(
        caches.keys().then(keys => {
            return Promise.all(keys
                .filter(key => key !== staticCacheName)
                .map(key => caches.delete(key))
                )
        })
    )
}); 

// fetch event
self.addEventListener('fetch', evt => {
    console.log('fetch event', evt);
    evt.respondWith(
        caches.match(evt.request).then(casheRes => {
            return casheRes || fetch(evt.request);/*.then(fetchRes => {
                return caches.open(dynamicCache).then(cache => {
                    cache.put(evt.request.url, fetchRes.clone());
                    return fetchRes;
                })
            });*/
        }).catch(() => {
            caches.match('/static/snake-game.html');
        })
    )
});