// ── Murmuration — boid flocking simulation ───────────────────────────────────

// Read CSS variables so boids match the current theme
function getCSSVar(name) {
    return getComputedStyle(document.body).getPropertyValue(name).trim();
}

// ── Vector helpers ────────────────────────────────────────────────────────────
class Vec {
    constructor(x = 0, y = 0) { this.x = x; this.y = y; }

    add(v)      { this.x += v.x; this.y += v.y; return this; }
    sub(v)      { return new Vec(this.x - v.x, this.y - v.y); }
    scale(s)    { this.x *= s;   this.y *= s;   return this; }
    copy()      { return new Vec(this.x, this.y); }
    mag()       { return Math.hypot(this.x, this.y); }

    setMag(m) {
        const n = this.mag();
        if (n > 0) { this.x = this.x / n * m; this.y = this.y / n * m; }
        return this;
    }

    limit(max) {
        if (this.mag() > max) this.setMag(max);
        return this;
    }

    static random2D() {
        const a = Math.random() * Math.PI * 2;
        return new Vec(Math.cos(a), Math.sin(a));
    }
}

// ── Boid ──────────────────────────────────────────────────────────────────────
class Boid {
    constructor(w, h) {
        this.pos = new Vec(Math.random() * w, Math.random() * h);
        this.vel = Vec.random2D().scale(Math.random() * 2 + 1);
        this.acc = new Vec();
    }

    // Wrap around canvas edges
    edges(w, h) {
        if (this.pos.x < 0)  this.pos.x = w;
        if (this.pos.x > w)  this.pos.x = 0;
        if (this.pos.y < 0)  this.pos.y = h;
        if (this.pos.y > h)  this.pos.y = 0;
    }

    // Steer toward a target velocity/position
    _steer(desired, maxSpeed, maxForce) {
        return desired.setMag(maxSpeed).sub(this.vel).limit(maxForce);
    }

    separation(boids, radius, maxSpeed, maxForce) {
        const steer = new Vec();
        let count = 0;
        for (const other of boids) {
            const d = Math.hypot(this.pos.x - other.pos.x, this.pos.y - other.pos.y);
            if (other !== this && d < radius && d > 0) {
                const diff = this.pos.sub(other.pos).scale(1 / (d * d));
                steer.add(diff);
                count++;
            }
        }
        if (count === 0) return steer;
        steer.scale(1 / count);
        return this._steer(steer, maxSpeed, maxForce);
    }

    alignment(boids, radius, maxSpeed, maxForce) {
        const avg = new Vec();
        let count = 0;
        for (const other of boids) {
            const d = Math.hypot(this.pos.x - other.pos.x, this.pos.y - other.pos.y);
            if (other !== this && d < radius) { avg.add(other.vel); count++; }
        }
        if (count === 0) return avg;
        avg.scale(1 / count);
        return this._steer(avg, maxSpeed, maxForce);
    }

    cohesion(boids, radius, maxSpeed, maxForce) {
        const center = new Vec();
        let count = 0;
        for (const other of boids) {
            const d = Math.hypot(this.pos.x - other.pos.x, this.pos.y - other.pos.y);
            if (other !== this && d < radius) { center.add(other.pos); count++; }
        }
        if (count === 0) return center;
        center.scale(1 / count);
        return this._steer(center.sub(this.pos), maxSpeed, maxForce);
    }

    flock(boids, p) {
        this.acc = new Vec();
        this.acc.add(this.separation(boids, p.separationRadius, p.maxSpeed, p.maxForce).scale(p.separation));
        this.acc.add(this.alignment (boids, p.alignmentRadius,  p.maxSpeed, p.maxForce).scale(p.alignment));
        this.acc.add(this.cohesion  (boids, p.cohesionRadius,   p.maxSpeed, p.maxForce).scale(p.cohesion));
    }

    update(maxSpeed) {
        this.vel.add(this.acc).limit(maxSpeed);
        if (this.vel.mag() < 0.5) this.vel.setMag(0.5); // never fully stop
        this.pos.add(this.vel);
    }

    draw(ctx, size, color, trailOpacity) {
        const angle = Math.atan2(this.vel.y, this.vel.x);
        ctx.save();
        ctx.translate(this.pos.x, this.pos.y);
        ctx.rotate(angle);
        ctx.fillStyle = color;
        ctx.globalAlpha = 0.85;
        ctx.beginPath();
        ctx.moveTo( size * 2,  0);
        ctx.lineTo(-size,     -size * 0.7);
        ctx.lineTo(-size * 0.4, 0);
        ctx.lineTo(-size,      size * 0.7);
        ctx.closePath();
        ctx.fill();
        ctx.restore();
    }
}

// ── Simulation state ──────────────────────────────────────────────────────────
const canvas = document.getElementById('murmuration-canvas');
const ctx    = canvas.getContext('2d');

let boids  = [];
let params = {};
let animId = null;
let running = true;

function defaultParams() {
    return {
        count:            150,
        separation:       1.5,
        alignment:        1.0,
        cohesion:         1.0,
        separationRadius: 28,
        alignmentRadius:  60,
        cohesionRadius:   60,
        maxSpeed:         3.5,
        maxForce:         0.12,
        boidSize:         5,
        trailLength:      0,    // 0 = no trail (future feature)
    };
}

function initBoids() {
    boids = [];
    for (let i = 0; i < params.count; i++) {
        boids.push(new Boid(canvas.width, canvas.height));
    }
}

function resizeCanvas() {
    canvas.width  = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    initBoids();
}

function boidColor() {
    return getCSSVar('--alt-color') || '#7c8cee';
}

function loop() {
    // Slight fade trail (set alpha < 1 to see trails)
    ctx.fillStyle = getCSSVar('--card-bg') || '#141720';
    ctx.globalAlpha = 0.35;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.globalAlpha = 1;

    const color = boidColor();
    for (const b of boids) {
        b.flock(boids, params);
        b.update(params.maxSpeed);
        b.edges(canvas.width, canvas.height);
        b.draw(ctx, params.boidSize, color);
    }

    if (running) animId = requestAnimationFrame(loop);
}

function start() {
    params = defaultParams();
    resizeCanvas();
    if (animId) cancelAnimationFrame(animId);
    running = true;
    loop();
}

// ── Controls ──────────────────────────────────────────────────────────────────
function bindControls() {
    const controls = [
        { id: 'ctrl-count',        param: 'count',            isInt: true,  onChange: initBoids },
        { id: 'ctrl-separation',   param: 'separation' },
        { id: 'ctrl-alignment',    param: 'alignment' },
        { id: 'ctrl-cohesion',     param: 'cohesion' },
        { id: 'ctrl-sep-radius',   param: 'separationRadius', isInt: true },
        { id: 'ctrl-align-radius', param: 'alignmentRadius',  isInt: true },
        { id: 'ctrl-coh-radius',   param: 'cohesionRadius',   isInt: true },
        { id: 'ctrl-speed',        param: 'maxSpeed' },
    ];

    for (const { id, param, isInt, onChange } of controls) {
        const input = document.getElementById(id);
        const label = document.getElementById(id + '-val');
        if (!input) continue;

        input.value = params[param];
        if (label) label.textContent = params[param];

        input.addEventListener('input', () => {
            const val = isInt ? parseInt(input.value) : parseFloat(input.value);
            params[param] = val;
            if (label) label.textContent = val;
            if (onChange) onChange();
        });
    }

    const pauseBtn = document.getElementById('btn-pause');
    const resetBtn = document.getElementById('btn-reset');

    if (pauseBtn) {
        pauseBtn.addEventListener('click', () => {
            running = !running;
            pauseBtn.textContent = running ? 'Pause' : 'Resume';
            if (running) loop();
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            params = defaultParams();
            syncControlsToParams(controls);
            initBoids();
            if (!running) { running = true; if (pauseBtn) pauseBtn.textContent = 'Pause'; loop(); }
        });
    }
}

function syncControlsToParams(controls) {
    for (const { id, param } of controls) {
        const input = document.getElementById(id);
        const label = document.getElementById(id + '-val');
        if (input) input.value = params[param];
        if (label) label.textContent = params[param];
    }
}

// ── Boot ──────────────────────────────────────────────────────────────────────
window.addEventListener('resize', () => {
    resizeCanvas();
});

document.addEventListener('DOMContentLoaded', () => {
    start();
    bindControls();
});
