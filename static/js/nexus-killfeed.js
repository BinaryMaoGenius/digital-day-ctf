window.NexusFeed = {
    init: function() {
        if ($('#nexus-killfeed').length === 0) {
            $('body').append('<div id="nexus-killfeed"></div>');
        }
    },
    addLog: function(title, message) {
        this.init();
        var $entry = $('<div class="killfeed-entry"><span class="kf-title">' + title + '</span>: <span class="kf-message">' + message + '</span></div>');
        $('#nexus-killfeed').prepend($entry);
        
        setTimeout(function() {
            $entry.addClass('fading-out');
            setTimeout(function() {
                $entry.remove();
            }, 500); // Wait for the CSS transition to finish
        }, 12000); // Show for 12 seconds
    }
};

$(document).ready(function() {
    window.NexusFeed.init();
});
