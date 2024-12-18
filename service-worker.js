self.addEventListener('push', function(event) {
    const options = {
        body: event.data.text(),
        icon: 'https://rafaelbrandaocruz.github.io/favicon.ico',
        badge: 'https://rafaelbrandaocruz.github.io/badge.ico',
    };

    event.waitUntil(
        self.registration.showNotification('Mudança no Site!', options)
    );
});

// Ativar o Service Worker e pedir permissão para notificações
self.addEventListener('install', function(event) {
    event.waitUntil(
        self.skipWaiting()
    );
});
