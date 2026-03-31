// background.js — landscape · boids · weather
// All visual effects in one canvas, fixed behind all page content.
(function () {
    'use strict';

    // ── Parse scene from body classes ─────────────────────────────────────────
    const cls = document.body.classList;
    const PERIODS    = ['night','dawn','morning','noon','afternoon','dusk'];
    const CONDITIONS = ['clear','clouds','rain','storm','snow','fog'];
    const period    = PERIODS.find(p => cls.contains('time-' + p))    || 'night';
    const condition = CONDITIONS.find(c => cls.contains('weather-' + c)) || 'clear';
    const isDark    = ['night','dawn','dusk'].includes(period);

    // ── Colour palettes ───────────────────────────────────────────────────────
    // skyTop/skyBot: hex gradient; mtnFar/mtnNear/hills/ground: [r,g,b];
    // boids: rgba string; stars: bool
    const PAL = {
        night: {
            skyTop:'#010306', skyBot:'#060d1c',
            mtnFar:[14,20,36], mtnNear:[10,14,26], hills:[7,9,18], ground:[5,7,13],
            boidColor:'rgba(155,185,235,0.72)', stars:true,
        },
        dawn: {
            skyTop:'#1c0e2e', skyBot:'#d94f60',
            mtnFar:[50,24,62], mtnNear:[26,11,40], hills:[15,7,24], ground:[10,5,15],
            boidColor:'rgba(245,180,195,0.76)', stars:false,
        },
        morning: {
            skyTop:'#3e90d2', skyBot:'#f6d24e',
            mtnFar:[108,128,154], mtnNear:[58,85,68], hills:[38,68,48], ground:[28,54,36],
            boidColor:'rgba(20,30,50,0.82)', stars:false,
        },
        noon: {
            skyTop:'#1462c4', skyBot:'#82c2ec',
            mtnFar:[78,110,136], mtnNear:[44,76,58], hills:[26,68,42], ground:[18,56,32],
            boidColor:'rgba(16,26,46,0.86)', stars:false,
        },
        afternoon: {
            skyTop:'#3282bc', skyBot:'#ecb030',
            mtnFar:[110,96,76], mtnNear:[62,58,40], hills:[48,48,28], ground:[36,44,24],
            boidColor:'rgba(20,26,42,0.82)', stars:false,
        },
        dusk: {
            skyTop:'#150920', skyBot:'#dc4210',
            mtnFar:[50,18,30], mtnNear:[28,11,20], hills:[15,7,11], ground:[10,5,7],
            boidColor:'rgba(242,150,108,0.76)', stars:false,
        },
    };
    const pal = PAL[period];

    // Sky darkening overlay for bad weather
    const wxDark = {clear:0, clouds:0.14, rain:0.26, storm:0.48, snow:0.07, fog:0}[condition] || 0;

    // ── Canvas setup ──────────────────────────────────────────────────────────
    const canvas = document.createElement('canvas');
    canvas.id = 'background-canvas';
    canvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;z-index:-1;pointer-events:none;';
    document.body.insertBefore(canvas, document.body.firstChild);
    const ctx = canvas.getContext('2d');

    let W = 0, H = 0;
    const HORIZON = 0.68;   // horizon line as fraction of H
    const SKY_TOP = 0.04;   // boids stay above this
    const SKY_BOT = 0.60;   // boids stay below this

    // ── Terrain keypoints (x, y) as fractions of W/H ─────────────────────────
    // Far range — distant mountains on the right, low hills on the left
    const FAR_MTN = [
        // Left — low rolling hills giving way to open sky
        [0.00,0.61],[0.08,0.57],[0.16,0.61],[0.24,0.56],[0.32,0.60],
        // Gentle transition rising right
        [0.42,0.54],[0.50,0.50],
        // Distant mountain range on right — tighter ridge, shallower valleys
        [0.54,0.50],[0.58,0.45],[0.62,0.49],[0.66,0.44],[0.70,0.48],
        [0.74,0.43],[0.78,0.47],[0.82,0.44],[0.86,0.48],[0.90,0.45],
        [0.94,0.49],[0.98,0.46],[1.00,0.55],
    ];
    // Foreground hills — original
    const HILLS = [
        [0.00,0.64],[0.11,0.57],[0.24,0.62],[0.37,0.54],[0.51,0.60],
        [0.63,0.55],[0.75,0.59],[0.88,0.56],[1.00,0.63],
    ];

    function rgba(arr, a = 1) { return `rgba(${arr[0]},${arr[1]},${arr[2]},${a})`; }

    function drawMtnPath(pts) {
        // Jagged mountains — straight lines between peaks
        ctx.beginPath();
        ctx.moveTo(0, H);
        for (const [x, y] of pts) ctx.lineTo(x * W, y * H);
        ctx.lineTo(W, H);
        ctx.closePath();
    }

    function drawHillPath(pts) {
        // Smooth hills — quadratic bezier using midpoints
        ctx.beginPath();
        ctx.moveTo(0, H);
        ctx.lineTo(0, pts[0][1] * H);
        for (let i = 0; i < pts.length - 1; i++) {
            const mx = ((pts[i][0] + pts[i+1][0]) / 2) * W;
            const my = ((pts[i][1] + pts[i+1][1]) / 2) * H;
            ctx.quadraticCurveTo(pts[i][0]*W, pts[i][1]*H, mx, my);
        }
        const last = pts[pts.length - 1];
        ctx.lineTo(last[0]*W, last[1]*H);
        ctx.lineTo(W, H);
        ctx.closePath();
    }

    // ── Stars ─────────────────────────────────────────────────────────────────
    let stars = [];
    function initStars() {
        stars = [];
        if (!pal.stars) return;
        for (let i = 0; i < 240; i++) {
            stars.push({
                x: Math.random(), y: Math.random() * 0.60,
                r: 0.3 + Math.random() * 1.4,
                op: 0.2 + Math.random() * 0.55,
                ph: Math.random() * Math.PI * 2,
            });
        }
    }

    function drawStars(t) {
        if (!stars.length) return;
        ctx.fillStyle = '#ffffff';
        for (const s of stars) {
            ctx.globalAlpha = s.op * (0.5 + 0.5 * Math.sin(t * 0.0007 + s.ph));
            ctx.beginPath();
            ctx.arc(s.x * W, s.y * H, s.r, 0, Math.PI * 2);
            ctx.fill();
        }
        ctx.globalAlpha = 1;
    }

    // ── Sun / moon ────────────────────────────────────────────────────────────
    const SUN_CFG = {
        dawn:      { x:0.10, y:0.84, col:'255,130,92',  op:0.28 },
        morning:   { x:0.22, y:0.28, col:'255,205,78',  op:0.20 },
        noon:      { x:0.50, y:0.02, col:'255,242,140', op:0.16 },
        afternoon: { x:0.76, y:0.26, col:'255,185,58',  op:0.20 },
        dusk:      { x:0.90, y:0.84, col:'255,76,26',   op:0.28 },
    };
    const wxSunScale = {clear:1.0,clouds:0.3,rain:0.1,storm:0.0,snow:0.4,fog:0.18}[condition] || 1;

    function drawSun() {
        const cfg = SUN_CFG[period];
        if (!cfg || wxSunScale === 0) return;
        const cx = cfg.x * W, cy = cfg.y * H;
        const r  = Math.max(W, H) * 0.56;
        const op = cfg.op * wxSunScale;

        const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, r);
        g.addColorStop(0,    `rgba(${cfg.col},${op.toFixed(3)})`);
        g.addColorStop(0.25, `rgba(${cfg.col},${(op*0.65).toFixed(3)})`);
        g.addColorStop(0.65, `rgba(${cfg.col},${(op*0.12).toFixed(3)})`);
        g.addColorStop(1,    `rgba(${cfg.col},0)`);
        ctx.fillStyle = g;
        ctx.fillRect(0, 0, W, H);

        const cr = r * 0.09;
        const cg = ctx.createRadialGradient(cx, cy, 0, cx, cy, cr);
        cg.addColorStop(0,  `rgba(255,252,218,${Math.min(op * 2.2, 0.60).toFixed(3)})`);
        cg.addColorStop(1,  'rgba(255,252,218,0)');
        ctx.fillStyle = cg;
        ctx.fillRect(0, 0, W, H);
    }

    // ── Landscape draw ────────────────────────────────────────────────────────
    function drawLandscape() {
        // Sky gradient
        const sg = ctx.createLinearGradient(0, 0, 0, H * HORIZON);
        sg.addColorStop(0, pal.skyTop);
        sg.addColorStop(1, pal.skyBot);
        ctx.fillStyle = sg;
        ctx.fillRect(0, 0, W, H * HORIZON + 2);

        // Weather sky darkening
        if (wxDark > 0) {
            ctx.fillStyle = `rgba(48,58,78,${wxDark})`;
            ctx.fillRect(0, 0, W, H * HORIZON + 2);
        }

        // Sun/moon (above terrain)
        drawSun();

        // Far mountains
        drawMtnPath(FAR_MTN);
        ctx.fillStyle = rgba(pal.mtnFar);
        ctx.fill();

        // Mid-range (same hill path shifted up slightly for depth)
        const midHills = HILLS.map(([x, y]) => [x, y * 0.88 + 0.01]);
        drawHillPath(midHills);
        ctx.fillStyle = rgba(pal.mtnNear);
        ctx.fill();

        // Foreground hills
        drawHillPath(HILLS);
        ctx.fillStyle = rgba(pal.hills);
        ctx.fill();

        // Ground fill
        ctx.fillStyle = rgba(pal.ground);
        ctx.fillRect(0, H * HORIZON - 1, W, H * (1 - HORIZON) + 2);
    }

    // ── Weather particles ─────────────────────────────────────────────────────
    let drops = [], snowFlakes = [], fogBlobs = [], windStreaks = [];

    function initWeather() {
        drops = []; snowFlakes = []; fogBlobs = []; windStreaks = [];

        if (condition === 'rain' || condition === 'storm') {
            const isStorm = condition === 'storm';
            const n = Math.floor(W / (isStorm ? 4 : 8));
            for (let i = 0; i < n; i++) {
                drops.push({ x:Math.random()*W, y:Math.random()*H,
                    len:10+Math.random()*(isStorm?18:10),
                    speed:5+Math.random()*(isStorm?10:5),
                    op:0.10+Math.random()*0.26 });
            }
            const ns = isStorm ? 55 : 26;
            for (let i = 0; i < ns; i++) {
                windStreaks.push({ x:-100+Math.random()*W, y:Math.random()*H,
                    len:40+Math.random()*(isStorm?130:75),
                    speed:10+Math.random()*(isStorm?22:13),
                    op:0.04+Math.random()*(isStorm?0.13:0.08) });
            }
        }

        if (condition === 'snow') {
            const n = Math.floor(W / 9);
            const [opMin, opMax] = isDark ? [0.30, 0.75] : [0.55, 0.92];
            const rMin = isDark ? 1.0 : 1.5, rMax = isDark ? 4.0 : 5.0;
            for (let i = 0; i < n; i++) {
                snowFlakes.push({ x:Math.random()*W, y:Math.random()*H,
                    r:rMin+Math.random()*(rMax-rMin),
                    speed:0.4+Math.random()*0.9, drift:Math.random()*0.5-0.25,
                    op:opMin+Math.random()*(opMax-opMin) });
            }
        }

        if (condition === 'fog') {
            const [opMin, opMax] = isDark ? [0.08, 0.20] : [0.18, 0.38];
            for (let i = 0; i < 24; i++) {
                fogBlobs.push({ x:-200+Math.random()*(W+400), y:Math.random()*H,
                    r:200+Math.random()*290, speed:0.10+Math.random()*0.28,
                    op:opMin+Math.random()*(opMax-opMin) });
            }
        }
    }

    // ── Lightning ─────────────────────────────────────────────────────────────
    if (condition === 'storm') {
        (function flash() {
            const el = document.createElement('div');
            el.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:600;background:rgba(192,218,255,0.65);';
            document.body.appendChild(el);
            setTimeout(() => { el.style.opacity='0'; },   65);
            setTimeout(() => { el.style.opacity='0.36'; }, 130);
            setTimeout(() => { el.style.opacity='0'; },   245);
            setTimeout(() => { el.remove(); },              310);
            setTimeout(flash, 5500 + Math.random() * 16000);
        }());
    }

    // ── Fog (drawn behind boids) ──────────────────────────────────────────────
    function drawFog() {
        const fc = isDark ? '198,204,218' : '72,88,106';
        for (const b of fogBlobs) {
            const g = ctx.createRadialGradient(b.x, b.y, 0, b.x, b.y, b.r);
            g.addColorStop(0,    `rgba(${fc},${b.op})`);
            g.addColorStop(0.5,  `rgba(${fc},${(b.op*0.48).toFixed(3)})`);
            g.addColorStop(1,    `rgba(${fc},0)`);
            ctx.fillStyle = g;
            ctx.beginPath();
            ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
            ctx.fill();
            b.x += b.speed;
            if (b.x - b.r > W) { b.x = -b.r - Math.random()*200; b.y = Math.random()*H; }
        }
    }

    // ── Rain / wind / snow (drawn in front of boids) ──────────────────────────
    const rainCol   = isDark ? '#a5c6e6' : '#466e96';
    const windCol   = isDark ? (condition==='storm'?'rgba(175,208,238,0.13)':'rgba(185,215,240,0.09)')
                             : (condition==='storm'?'rgba(44,72,108,0.11)' :'rgba(55,85,118,0.08)');

    function drawPrecip() {
        // Rain drops
        if (drops.length) {
            const ax = condition === 'storm' ? 0.24 : 0.11;
            ctx.strokeStyle = rainCol; ctx.lineWidth = 1;
            for (const d of drops) {
                ctx.globalAlpha = d.op;
                ctx.beginPath();
                ctx.moveTo(d.x, d.y);
                ctx.lineTo(d.x - d.len * ax, d.y + d.len);
                ctx.stroke();
                d.y += d.speed; d.x -= d.speed * ax;
                if (d.y > H) { d.y = -d.len; d.x = Math.random() * W; }
            }
        }
        // Wind streaks
        if (windStreaks.length) {
            ctx.strokeStyle = windCol; ctx.lineWidth = 1;
            for (const s of windStreaks) {
                ctx.globalAlpha = s.op;
                ctx.beginPath();
                ctx.moveTo(s.x, s.y);
                ctx.lineTo(s.x + s.len, s.y + s.len * 0.06);
                ctx.stroke();
                s.x += s.speed;
                if (s.x > W + s.len) { s.x = -s.len - Math.random()*300; s.y = Math.random()*H; }
            }
        }
        // Snow
        for (const f of snowFlakes) {
            ctx.globalAlpha = f.op;
            ctx.fillStyle = '#ffffff';
            ctx.beginPath();
            ctx.arc(f.x, f.y, f.r, 0, Math.PI * 2);
            ctx.fill();
            f.y += f.speed; f.x += f.drift;
            if (f.y > H + f.r) { f.y = -f.r; f.x = Math.random()*W; }
            if (f.x >  W + f.r) f.x = -f.r;
            if (f.x < -f.r)     f.x =  W + f.r;
        }
        ctx.globalAlpha = 1;
    }

    // ── Vec + Boid ────────────────────────────────────────────────────────────
    class Vec {
        constructor(x=0,y=0){this.x=x;this.y=y;}
        add(v){this.x+=v.x;this.y+=v.y;return this;}
        sub(v){return new Vec(this.x-v.x,this.y-v.y);}
        scale(s){this.x*=s;this.y*=s;return this;}
        mag(){return Math.hypot(this.x,this.y);}
        setMag(m){const n=this.mag();if(n>0){this.x=this.x/n*m;this.y=this.y/n*m;}return this;}
        limit(m){if(this.mag()>m)this.setMag(m);return this;}
        static rand2D(){const a=Math.random()*Math.PI*2;return new Vec(Math.cos(a),Math.sin(a));}
    }

    class Boid {
        constructor() {
            this.pos = new Vec(Math.random()*W, (SKY_TOP + Math.random()*(SKY_BOT-SKY_TOP))*H);
            this.vel = Vec.rand2D().scale(1 + Math.random()*2);
            this.acc = new Vec();
        }
        steer(des) {
            const p = window.murmuParams;
            return des.setMag(p.maxSpeed).sub(this.vel).limit(p.maxForce);
        }
        separation(all) {
            const r = window.murmuParams.separationRadius;
            const s = new Vec(); let n = 0;
            for (const o of all) {
                const d = Math.hypot(this.pos.x-o.pos.x, this.pos.y-o.pos.y);
                if (o!==this && d<r && d>0) { s.add(this.pos.sub(o.pos).scale(1/(d*d))); n++; }
            }
            if (!n) return s;
            return this.steer(s.scale(1/n));
        }
        alignment(all) {
            const r = window.murmuParams.alignmentRadius;
            const v = new Vec(); let n = 0;
            for (const o of all) {
                const d = Math.hypot(this.pos.x-o.pos.x, this.pos.y-o.pos.y);
                if (o!==this && d<r) { v.add(o.vel); n++; }
            }
            if (!n) return v;
            return this.steer(v.scale(1/n));
        }
        cohesion(all) {
            const r = window.murmuParams.cohesionRadius;
            const c = new Vec(); let n = 0;
            for (const o of all) {
                const d = Math.hypot(this.pos.x-o.pos.x, this.pos.y-o.pos.y);
                if (o!==this && d<r) { c.add(o.pos); n++; }
            }
            if (!n) return c;
            return this.steer(c.scale(1/n).sub(this.pos));
        }
        flock(all) {
            const p = window.murmuParams;
            this.acc = new Vec();
            this.acc.add(this.separation(all).scale(p.separation));
            this.acc.add(this.alignment(all).scale(p.alignment));
            this.acc.add(this.cohesion(all).scale(p.cohesion));
            // Soft sky boundary
            if (this.pos.y < SKY_TOP * H) this.acc.add(new Vec(0,  p.maxForce * 4));
            if (this.pos.y > SKY_BOT * H) this.acc.add(new Vec(0, -p.maxForce * 4));
        }
        update() {
            const p = window.murmuParams;
            this.vel.add(this.acc).limit(p.maxSpeed);
            if (this.vel.mag() < 0.5) this.vel.setMag(0.5);
            this.pos.add(this.vel);
            // Horizontal wrap
            if (this.pos.x <  0) this.pos.x = W;
            if (this.pos.x > W) this.pos.x = 0;
        }
        draw(size, color) {
            const a = Math.atan2(this.vel.y, this.vel.x);
            ctx.save();
            ctx.translate(this.pos.x, this.pos.y);
            ctx.rotate(a);
            ctx.fillStyle = color;
            ctx.globalAlpha = 0.84;
            ctx.beginPath();
            ctx.moveTo( size*2,  0);
            ctx.lineTo(-size,   -size*0.7);
            ctx.lineTo(-size*0.4, 0);
            ctx.lineTo(-size,    size*0.7);
            ctx.closePath();
            ctx.fill();
            ctx.restore();
        }
    }

    // ── Global boid params (readable/writable by murmuration controls) ────────
    window.murmuParams = {
        count:200, separation:1.5, alignment:1.0, cohesion:1.0,
        separationRadius:28, alignmentRadius:60, cohesionRadius:60,
        maxSpeed:1.5, maxForce:0.12, boidSize:4,
    };

    let boids = [];
    window.reinitBoids = function () {
        boids = [];
        for (let i = 0; i < window.murmuParams.count; i++) boids.push(new Boid());
    };

    // ── Resize ────────────────────────────────────────────────────────────────
    function resize() {
        W = canvas.width  = window.innerWidth;
        H = canvas.height = window.innerHeight;
        initStars();
        initWeather();
        window.reinitBoids();
    }
    window.addEventListener('resize', resize);
    resize();

    // ── Main loop ─────────────────────────────────────────────────────────────
    let t = 0;
    function loop() {
        t++;
        ctx.clearRect(0, 0, W, H);

        drawLandscape();
        drawStars(t);
        drawFog();

        // Boids
        const p = window.murmuParams;
        for (const b of boids) { b.flock(boids); b.update(); b.draw(p.boidSize, pal.boidColor); }

        drawPrecip();

        requestAnimationFrame(loop);
    }

    loop();
}());
