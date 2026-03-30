// murmuration.js — controls only
// Reads/writes window.murmuParams defined in background.js and triggers reinit on count change.
(function () {
    'use strict';

    function bindSlider(id, valId, paramKey) {
        const slider = document.getElementById(id);
        const display = document.getElementById(valId);
        if (!slider || !display) return;

        // Sync display to initial slider value
        display.textContent = slider.value;

        slider.addEventListener('input', function () {
            display.textContent = this.value;
            if (window.murmuParams) window.murmuParams[paramKey] = +this.value;
        });
    }

    function init() {
        if (!window.murmuParams) {
            // background.js not yet ready — retry
            setTimeout(init, 50);
            return;
        }

        bindSlider('ctrl-count',       'ctrl-count-val',       'count');
        bindSlider('ctrl-speed',       'ctrl-speed-val',       'maxSpeed');
        bindSlider('ctrl-separation',  'ctrl-separation-val',  'separation');
        bindSlider('ctrl-sep-radius',  'ctrl-sep-radius-val',  'separationRadius');
        bindSlider('ctrl-alignment',   'ctrl-alignment-val',   'alignment');
        bindSlider('ctrl-align-radius','ctrl-align-radius-val','alignmentRadius');
        bindSlider('ctrl-cohesion',    'ctrl-cohesion-val',    'cohesion');
        bindSlider('ctrl-coh-radius',  'ctrl-coh-radius-val',  'cohesionRadius');

        // Count change needs full boid reinit
        const countSlider = document.getElementById('ctrl-count');
        if (countSlider) {
            countSlider.addEventListener('change', function () {
                if (window.murmuParams) window.murmuParams.count = +this.value;
                if (window.reinitBoids) window.reinitBoids();
            });
        }

        // Reset restores background.js defaults
        const btnReset = document.getElementById('btn-reset');
        if (btnReset) {
            btnReset.addEventListener('click', function () {
                const defaults = {
                    count: 120, maxSpeed: 3.2,
                    separation: 1.5, separationRadius: 28,
                    alignment: 1.0, alignmentRadius: 60,
                    cohesion: 1.0,  cohesionRadius: 60,
                };
                Object.assign(window.murmuParams, defaults);

                const map = {
                    'ctrl-count':       ['ctrl-count-val',       'count'],
                    'ctrl-speed':       ['ctrl-speed-val',       'maxSpeed'],
                    'ctrl-separation':  ['ctrl-separation-val',  'separation'],
                    'ctrl-sep-radius':  ['ctrl-sep-radius-val',  'separationRadius'],
                    'ctrl-alignment':   ['ctrl-alignment-val',   'alignment'],
                    'ctrl-align-radius':['ctrl-align-radius-val','alignmentRadius'],
                    'ctrl-cohesion':    ['ctrl-cohesion-val',    'cohesion'],
                    'ctrl-coh-radius':  ['ctrl-coh-radius-val',  'cohesionRadius'],
                };
                Object.entries(map).forEach(([sliderId, [displayId, key]]) => {
                    const s = document.getElementById(sliderId);
                    const d = document.getElementById(displayId);
                    if (s) s.value = defaults[key];
                    if (d) d.textContent = defaults[key];
                });

                if (window.reinitBoids) window.reinitBoids();
            });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
