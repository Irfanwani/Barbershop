const staticCacheName = 'site-static';
const assets = [
    '/',
    '/static/images',
    '/static/app.js'
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
}); 

// fetch event
self.addEventListener('fetch', evt => {
    //console.log('fetch event', evt);
});