// installation event
self.addEventListener('install', evt => {
    console.log('Service worker has been installed.');
});

// activation event
self.addEventListener('activate', evt => {
    console.log('Service worker has been activated.');
}); 

// fetch event
self.addEventListener('fetch', evt => {
    console.log('fetch event', evt);
});