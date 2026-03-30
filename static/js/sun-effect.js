(function () {
    const classes = document.body.classList;

    const PERIODS    = ['night', 'dawn', 'morning', 'noon', 'afternoon', 'dusk'];
    const CONDITIONS = ['clear', 'clouds', 'rain', 'storm', 'snow', 'fog'];

    const period    = PERIODS.find(p => classes.contains('time-' + p))    || 'night';
    const condition = CONDITIONS.find(c => classes.contains('weather-' + c)) || 'clear';

    if (period === 'night') return;

    // How much each weather condition attenuates the sun
    const weatherScale = {
        clear:  1.00,
        clouds: 0.30,
        rain:   0.10,
        storm:  0.00,
        snow:   0.40,
        fog:    0.18,
    }[condition];

    if (weatherScale === 0) return;

    // Sun position (0–1 of screen), glow radius (fraction of max dimension),
    // core color, and base opacity per time period
    const config = {
        dawn:      { x: 0.10, y: 0.85, r: 0.55, color: '255,130,90',  opacity: 0.28 },
        morning:   { x: 0.22, y: 0.30, r: 0.60, color: '255,205,80',  opacity: 0.20 },
        noon:      { x: 0.50, y: 0.00, r: 0.65, color: '255,240,140', opacity: 0.16 },
        afternoon: { x: 0.75, y: 0.25, r: 0.60, color: '255,185,60',  opacity: 0.20 },
        dusk:      { x: 0.90, y: 0.85, r: 0.55, color: '255,80,30',   opacity: 0.30 },
    }[period];

    if (!config) return;

    const canvas = document.createElement('canvas');
    canvas.style.cssText = [
        'position:fixed', 'top:0', 'left:0',
        'width:100%', 'height:100%',
        'pointer-events:none',
        'z-index:400',
    ].join(';');
    document.body.appendChild(canvas);
    const ctx = canvas.getContext('2d');

    function draw() {
        canvas.width  = window.innerWidth;
        canvas.height = window.innerHeight;

        const cx = config.x * canvas.width;
        const cy = config.y * canvas.height;
        const r  = config.r * Math.max(canvas.width, canvas.height);
        const op = config.opacity * weatherScale;

        // Outer atmospheric glow
        const glow = ctx.createRadialGradient(cx, cy, 0, cx, cy, r);
        glow.addColorStop(0,    `rgba(${config.color},${(op).toFixed(3)})`);
        glow.addColorStop(0.25, `rgba(${config.color},${(op * 0.65).toFixed(3)})`);
        glow.addColorStop(0.6,  `rgba(${config.color},${(op * 0.18).toFixed(3)})`);
        glow.addColorStop(1,    `rgba(${config.color},0)`);
        ctx.fillStyle = glow;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Bright inner core (small tight disc)
        const coreR = r * 0.10;
        const core  = ctx.createRadialGradient(cx, cy, 0, cx, cy, coreR);
        core.addColorStop(0,   `rgba(255,255,230,${Math.min(op * 1.8, 0.55).toFixed(3)})`);
        core.addColorStop(0.5, `rgba(255,245,200,${(op * 0.5).toFixed(3)})`);
        core.addColorStop(1,   'rgba(255,245,200,0)');
        ctx.fillStyle = core;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    draw();
    window.addEventListener('resize', draw);
})();
