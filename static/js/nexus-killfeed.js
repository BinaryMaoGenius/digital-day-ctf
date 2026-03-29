/**
 * Digital Day - Nexus Killfeed
 * Handles live event feeds (captures, updates) with cyberpunk typing and glitch effects.
 */

window.NexusFeed = (function() {
    const feedContainerId = 'nexus-killfeed';
    const maxLogs = 5; // Maximum number of logs to display before fading out the old ones
    
    // Initialize the container if it doesn't exist
    function init() {
        if (!document.getElementById(feedContainerId)) {
            const container = document.createElement('div');
            container.id = feedContainerId;
            document.body.appendChild(container);
        }
    }

    // Play a subtle sound effect on new feed (bip)
    function playBeep() {
        // Create an oscillator based beep for that authentic terminal feel
        try {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            
            osc.connect(gain);
            gain.connect(ctx.destination);
            
            osc.type = 'square';
            osc.frequency.setValueAtTime(800, ctx.currentTime); // 800Hz
            osc.frequency.exponentialRampToValueAtTime(400, ctx.currentTime + 0.1);
            
            gain.gain.setValueAtTime(0.05, ctx.currentTime); // Very low volume
            gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.1);
            
            osc.start(ctx.currentTime);
            osc.stop(ctx.currentTime + 0.1);
        } catch(e) {
            // AudioContext not supported or blocked by browser policy without user interaction
        }
    }

    // Add a new log to the killfeed
    function addLog(title, message) {
        init();
        const container = document.getElementById(feedContainerId);
        
        // Create the entry container
        const entry = document.createElement('div');
        entry.className = 'killfeed-entry new-entry';
        
        // Format the message
        let htmlContent = '';
        if (title) htmlContent += `<span class="kf-title">[${title}]</span> `;
        if (message) htmlContent += `<span class="kf-message">${message}</span>`;
        
        entry.innerHTML = htmlContent;
        
        // Append to feed
        container.appendChild(entry);
        
        // Play sound
        playBeep();
        
        // Typing effect logic
        const chars = entry.innerText.split('');
        entry.innerHTML = ''; // Clear for typing
        
        let i = 0;
        const typingInterval = setInterval(() => {
            if (i < chars.length) {
                // Add character by character, restoring some basic HTML structure loosely
                entry.textContent += chars[i];
                i++;
            } else {
                clearInterval(typingInterval);
                entry.innerHTML = htmlContent; // Restore full HTML (colors) once typing completes
                entry.classList.remove('new-entry');
            }
        }, 15); // Fast typing speed

        // Manage max logs and remove oldest
        const logs = container.querySelectorAll('.killfeed-entry');
        if (logs.length > maxLogs) {
            const oldest = logs[0];
            oldest.classList.add('fading-out');
            setTimeout(() => {
                if(oldest.parentNode) oldest.remove();
            }, 500); // 0.5s fade out
        }
    }

    // Auto init on load
    document.addEventListener('DOMContentLoaded', init);

    return {
        addLog: addLog
    };
})();
