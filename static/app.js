if('serviceWorker' in navigator) {
    navigator.serviceWorker.register("/sw.js")
    .then(reg => console.log(reg, 'service worker registered.'))
    .catch(error => console.log(error, "service worker not registered."));
}