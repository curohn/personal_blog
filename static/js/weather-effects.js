(function () {
    const classes = document.body.classList;

    const isRain  = classes.contains('weather-rain');
    const isStorm = classes.contains('weather-storm');
    const isSnow  = classes.contains('weather-snow');
    const isFog   = classes.contains('weather-fog');

    if (!isRain && !isStorm && !isSnow && !isFog) return;

    const isDark = ['time-night','time-dawn','time-dusk'].some(c => classes.contains(c));

    // Colors tuned for legibility on both light and dark backgrounds
    const rainColor   = isDark ? '#a8c8e8' : '#4878a0';
    const streakColor = isDark ? (isStorm ? '#b8d0e8' : '#c8d8e8')
                               : (isStorm ? '#3a6888' : '#5888a8');
    const fogColor    = isDark ? '210,215,225' : '80,100,120';

    // ── canvas setup ──────────────────────────────────────────────────────────
    const canvas = document.createElement('canvas');
    canvas.style.cssText = [
        'position:fixed', 'top:0', 'left:0',
        'width:100%', 'height:100%',
        'pointer-events:none',
        'z-index:500',
    ].join(';');
    document.body.appendChild(canvas);
    const ctx = canvas.getContext('2d');

    let drops = [], streaks = [], flakes = [], fogBlobs = [];

    function resize() {
        canvas.width  = window.innerWidth;
        canvas.height = window.innerHeight;
        init();
    }

    function rand(min, max) { return Math.random() * (max - min) + min; }

    function init() {
        drops = []; streaks = []; flakes = []; fogBlobs = [];

        if (isSnow) {
            const count = Math.floor(canvas.width / 10);
            const opacityMin = isDark ? 0.2 : 0.5;
            const opacityMax = isDark ? 0.7 : 0.9;
            for (let i = 0; i < count; i++) {
                flakes.push({
                    x:       rand(0, canvas.width),
                    y:       rand(0, canvas.height),
                    r:       rand(isDark ? 1 : 1.5, isDark ? 4 : 5),
                    speed:   rand(0.4, 1.2),
                    drift:   rand(-0.3, 0.3),
                    opacity: rand(opacityMin, opacityMax),
                });
            }
        }

        if (isRain || isStorm) {
            const dropCount   = isStorm ? Math.floor(canvas.width / 4) : Math.floor(canvas.width / 8);
            const streakCount = isStorm ? 50 : 25;
            const angleX      = isStorm ? 0.25 : 0.12; // wind-driven angle

            for (let i = 0; i < dropCount; i++) {
                drops.push({
                    x:       rand(0, canvas.width),
                    y:       rand(0, canvas.height),
                    len:     rand(10, isStorm ? 22 : 16),
                    speed:   rand(5, isStorm ? 14 : 9),
                    angleX,
                    opacity: rand(0.1, 0.35),
                });
            }

            // Horizontal wind streaks
            for (let i = 0; i < streakCount; i++) {
                streaks.push({
                    x:       rand(-200, canvas.width),
                    y:       rand(0, canvas.height),
                    len:     rand(40, isStorm ? 120 : 70),
                    speed:   rand(10, isStorm ? 22 : 14),
                    opacity: rand(0.04, isStorm ? 0.14 : 0.08),
                });
            }
        }

        if (isFog) {
            const fogOpacityMin = isDark ? 0.08 : 0.18;
            const fogOpacityMax = isDark ? 0.18 : 0.35;
            for (let i = 0; i < 22; i++) {
                fogBlobs.push({
                    x:       rand(-200, canvas.width + 200),
                    y:       rand(0, canvas.height),
                    r:       rand(200, 420),
                    speed:   rand(0.12, 0.35),
                    opacity: rand(fogOpacityMin, fogOpacityMax),
                });
            }
        }
    }

    // ── lightning (storm only) ────────────────────────────────────────────────
    if (isStorm) {
        function flash() {
            const el = document.createElement('div');
            el.style.cssText = [
                'position:fixed', 'inset:0',
                'pointer-events:none', 'z-index:600',
                'background:rgba(190,215,255,0.65)',
                'transition:opacity 60ms',
            ].join(';');
            document.body.appendChild(el);

            // Double-flash sequence mimicking real lightning
            setTimeout(() => el.style.opacity = '0',    70);
            setTimeout(() => el.style.opacity = '0.38', 140);
            setTimeout(() => el.style.opacity = '0',    260);
            setTimeout(() => el.remove(),                320);

            setTimeout(flash, rand(5000, 18000));
        }
        setTimeout(flash, rand(1500, 6000));
    }

    // ── draw loop ─────────────────────────────────────────────────────────────
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Snow
        flakes.forEach(p => {
            ctx.globalAlpha = p.opacity;
            ctx.fillStyle = '#ffffff';
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fill();
            p.y += p.speed;
            p.x += p.drift;
            if (p.y > canvas.height + p.r) { p.y = -p.r; p.x = rand(0, canvas.width); }
            if (p.x >  canvas.width  + p.r)  p.x = -p.r;
            if (p.x < -p.r)                   p.x =  canvas.width + p.r;
        });

        // Rain drops
        ctx.strokeStyle = rainColor;
        ctx.lineWidth = 1;
        drops.forEach(p => {
            ctx.globalAlpha = p.opacity;
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p.x - p.len * p.angleX, p.y + p.len);
            ctx.stroke();
            p.y += p.speed;
            p.x -= p.speed * p.angleX;
            if (p.y > canvas.height + p.len) { p.y = -p.len; p.x = rand(0, canvas.width); }
        });

        // Wind streaks
        ctx.strokeStyle = streakColor;
        ctx.lineWidth = 1;
        streaks.forEach(s => {
            ctx.globalAlpha = s.opacity;
            ctx.beginPath();
            ctx.moveTo(s.x, s.y);
            ctx.lineTo(s.x + s.len, s.y + s.len * 0.06);
            ctx.stroke();
            s.x += s.speed;
            if (s.x > canvas.width + s.len) {
                s.x = -s.len - rand(0, 300);
                s.y = rand(0, canvas.height);
            }
        });

        // Fog blobs (radial gradient circles drifting slowly)
        fogBlobs.forEach(b => {
            const g = ctx.createRadialGradient(b.x, b.y, 0, b.x, b.y, b.r);
            g.addColorStop(0,   `rgba(${fogColor},${b.opacity})`);
            g.addColorStop(0.5, `rgba(${fogColor},${b.opacity * 0.55})`);
            g.addColorStop(1,   `rgba(${fogColor},0)`);
            ctx.globalAlpha = 1;
            ctx.fillStyle = g;
            ctx.beginPath();
            ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
            ctx.fill();
            b.x += b.speed;
            if (b.x - b.r > canvas.width) {
                b.x = -b.r - rand(0, 200);
                b.y = rand(0, canvas.height);
            }
        });

        ctx.globalAlpha = 1;
        requestAnimationFrame(draw);
    }

    window.addEventListener('resize', resize);
    resize();
    draw();
})();
