// Tactical Analysis Post Logic
document.addEventListener('DOMContentLoaded', function() {
    const analysisPanel = document.getElementById('tactical-analysis-panel');
    if (!analysisPanel) return;

    const category = analysisPanel.getAttribute('data-category');
    const boxUuid = analysisPanel.getAttribute('data-box-uuid');

    if (category === 'Stéganographie' || category === 'Steganography' || category === 'Forensics') {
        initSteganoView();
    } else if (category === 'Web' || category === 'Web Infiltration') {
        initWebView();
    }

    function initSteganoView() {
        analysisPanel.innerHTML = `
            <div class="glass-panel modern-card" style="margin-top: 20px;">
                <h3 class="mono accent-text" style="font-size: 1rem; margin-bottom: 15px;"><i class="fa fa-picture-o"></i> ANALYSE_VISUELLE</h3>
                <div style="display: flex; gap: 20px;">
                    <div id="stegano-container" style="flex: 1; background: #000; border: 1px solid var(--border-color); border-radius: 8px; overflow: hidden; position: relative;">
                        <img id="stegano-image" src="" style="width: 100%; display: block; filter: contrast(100%) brightness(100%);">
                        <div id="stegano-overlay" style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; pointer-events: none; mix-blend-mode: color-dodge; display: none; background: linear-gradient(rgba(18, 194, 233, 0.5), rgba(196, 113, 237, 0.5));"></div>
                    </div>
                    <div style="width: 200px;">
                        <button class="btn-modern steg-filter" data-filter="none" style="width: 100%; margin-bottom: 10px; font-size: 0.7rem;">ORIGINAL</button>
                        <button class="btn-modern steg-filter" data-filter="contrast(200%)" style="width: 100%; margin-bottom: 10px; font-size: 0.7rem;">HAUT_CONTRASTE</button>
                        <button class="btn-modern steg-filter" data-filter="invert(100%)" style="width: 100%; margin-bottom: 10px; font-size: 0.7rem;">INVERSION</button>
                        <button class="btn-modern steg-filter" data-filter="grayscale(100%)" style="width: 100%; margin-bottom: 10px; font-size: 0.7rem;">LUMINANCE</button>
                        <button class="btn-modern" id="toggle-overlay" style="width: 100%; font-size: 0.7rem; background: var(--accent-glow) !important; color: var(--accent-color) !important;">FILTRE_BOGOLAN</button>
                    </div>
                </div>
            </div>
        `;

        // Find materials that are images
        const materials = document.querySelectorAll('.jstree-anchor');
        materials.forEach(m => {
            if (m.innerText.match(/\.(png|jpg|jpeg|gif)$/i)) {
                const imgUrl = m.getAttribute('href'); // This might need fix depending on jstree
                // For now, let's just listen to clicks on jstree or use the first image found
            }
        });

        const img = document.getElementById('stegano-image');
        const filters = document.querySelectorAll('.steg-filter');
        filters.forEach(btn => {
            btn.addEventListener('click', () => {
                img.style.filter = btn.getAttribute('data-filter');
            });
        });

        document.getElementById('toggle-overlay').addEventListener('click', () => {
            const overlay = document.getElementById('stegano-overlay');
            overlay.style.display = overlay.style.display === 'none' ? 'block' : 'none';
        });
    }

    function initWebView() {
        analysisPanel.innerHTML = `
            <div class="glass-panel modern-card" style="margin-top: 20px;">
                <h3 class="mono accent-text" style="font-size: 1rem; margin-bottom: 15px;"><i class="fa fa-globe"></i> NAVIGATEUR_SÉCURISÉ</h3>
                <div style="background: #1a1a1a; border-radius: 8px; overflow: hidden; border: 1px solid var(--border-color);">
                    <div style="background: #333; padding: 5px 10px; display: flex; align-items: center; gap: 10px;">
                        <div style="display: flex; gap: 5px;">
                            <div style="width: 8px; height: 8px; border-radius: 50%; background: #ff5f56;"></div>
                            <div style="width: 8px; height: 8px; border-radius: 50%; background: #ffbd2e;"></div>
                            <div style="width: 8px; height: 8px; border-radius: 50%; background: #27c93f;"></div>
                        </div>
                        <div id="browser-url" class="mono" style="background: #000; padding: 2px 10px; flex: 1; font-size: 0.7rem; border-radius: 4px; color: #888;">http://localhost:8888/target/resource</div>
                    </div>
                    <div id="browser-viewport" style="height: 300px; background: #fff; position: relative;">
                         <iframe id="target-frame" src="" style="width: 100%; height: 100%; border: none;"></iframe>
                    </div>
                </div>
            </div>
        `;
    }
});
