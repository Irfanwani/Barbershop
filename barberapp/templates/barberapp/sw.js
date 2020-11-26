const staticCacheName = 'site-static';
const assets = [
    '/',
    '/static',
    'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css',
    'https://pro.fontawesome.com/releases/v5.10.0/css/all.css',
    'https://code.jquery.com/jquery-3.5.1.min.js',
    'https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.23.0/moment.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/tempusdominus-bootstrap-4/5.1.2/css/tempusdominus-bootstrap-4.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/tempusdominus-bootstrap-4/5.1.2/js/tempusdominus-bootstrap-4.min.js',
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