const NexusNotifications = {
    init: function() {
        if ("Notification" in window) {
            if (Notification.permission !== "granted" && Notification.permission !== "denied") {
                Notification.requestPermission();
            }
        }
    },

    notify: function(title, body) {
        if ("Notification" in window && Notification.permission === "granted") {
            new Notification(title, {
                body: body,
                icon: '/static/images/pwa-icon-192.png'
            });
        }
        // Fallback to internal notifier
        if (typeof(notify) === 'function') {
            notify(title, body, 'info');
        }
    }
};

$(document).ready(() => {
    NexusNotifications.init();
});
