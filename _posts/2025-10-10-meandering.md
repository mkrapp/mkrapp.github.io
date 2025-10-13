---
layout: post
title: "River Meandering"
author: "Mario"
date: 2025-10-10
usemathjax: true
---


Yesterday, I gave a guest lecture about climate change (past, present, future).

As a motivating example, I showed an aerial image that I took during a helicopter flight aorund [Aoraki / Mount Cook National Park](https://en.wikipedia.org/wiki/Aoraki_/_Mount_Cook_National_Park){:target="_blank"} in May.

![](/assets/aoraki.png)

There is so much structure in that image and I thought, "I could come up with an approximation for that river bed!".

A few hours later, I had a *phenomenological* model that would describe the main features of the river bed and the flow of the water within.

The toy model below has 3 main parameters, *displacement*, *decay*, and *max dimension*. You can try to match the real world by changing those. *water percentage* is a visual effect that color-codes a percentage of all lines in a watery color.

<span>Seed:</span>
<input id="seedInput" type="number" value="1234" style="width: 100px;">
<button id="randomizeBtn">Randomize Seed</button>

<label>
  Displacement
  <input id="dispSlider" type="range" min="0" max="1.2" step="0.05" value="0.3">
  <span id="dispVal">0.3</span>
</label>

<label>
  Decay
  <input id="decaySlider" type="range" min="0" max="1.2" step="0.05" value="0.8">
  <span id="decayVal">0.8</span>
</label>

<label>
  Max Dimension
  <input id="depthSlider" type="range" min="1" max="10" step="1" value="6">
  <span id="depthVal">6</span>
</label>

<label>
  Water Percentage
  <input id="probSlider" type="range" min="0" max="1" step="0.01" value="0.05">
  <span id="probVal">0.05</span>
</label>


<canvas id="riverCanvas"></canvas>

<script>
const canvas = document.getElementById("riverCanvas");
const ctx = canvas.getContext("2d");

// === Seeded RNG ===
function mulberry32(seed) {
  return function() {
    let t = seed += 0x6D2B79F5;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

let baseSeed = 1234;
let random = mulberry32(baseSeed);
function reseed() {
  random = mulberry32(baseSeed);
}
function randn() {
  let u = 0, v = 0;
  while (u === 0) u = random();
  while (v === 0) v = random();
  return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
}

function toCanvasCoords(x, y) {
  return [x / 10 * canvas.width, canvas.height - (y / 5 * canvas.height)];
}

function midpointMeander(start, end, depth, displacement, decay) {
  function subdivide(pts, level, disp) {
    if (level === 0) return pts;
    const newPts = [pts[0]];
    for (let i = 0; i < pts.length - 1; i++) {
      const a = pts[i];
      const b = pts[i + 1];
      const mid = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
      const dir = [b[0] - a[0], b[1] - a[1]];
      const length = Math.hypot(dir[0], dir[1]);
      let perp = [0, 0];
      if (length > 0) {
        perp = [-dir[1] / length, dir[0] / length];
      }
      const offsetMag = disp * Math.sqrt(length) * randn();
      const midShifted = [mid[0] + perp[0] * offsetMag, mid[1] + perp[1] * offsetMag];
      newPts.push(midShifted, b);
    }
    return subdivide(newPts, level - 1, disp * decay);
  }
  return subdivide([start, end], depth, displacement);
}

function chaikinSmoothing(points, iterations = 2) {
  let pts = points.slice();
  for (let it = 0; it < iterations; it++) {
    const newPts = [pts[0]];
    for (let i = 0; i < pts.length - 1; i++) {
      const p0 = pts[i], p1 = pts[i + 1];
      const q = [0.75 * p0[0] + 0.25 * p1[0], 0.75 * p0[1] + 0.25 * p1[1]];
      const r = [0.25 * p0[0] + 0.75 * p1[0], 0.25 * p0[1] + 0.75 * p1[1]];
      newPts.push(q, r);
    }
    newPts.push(pts[pts.length - 1]);
    pts = newPts;
  }
  return pts;
}

function drawRiver(points, color, alpha, width) {
  ctx.beginPath();
  const [x0, y0] = toCanvasCoords(points[0][0], points[0][1]);
  ctx.moveTo(x0, y0);
  for (let i = 1; i < points.length; i++) {
    const [x, y] = toCanvasCoords(points[i][0], points[i][1]);
    ctx.lineTo(x, y);
  }
  ctx.strokeStyle = color;
  ctx.globalAlpha = alpha;
  ctx.lineWidth = width;
  ctx.stroke();
  ctx.globalAlpha = 1.0;
}

function drawRivers(displacement, decay, prob, maxDepth) {
  reseed(); // reset RNG for deterministic behavior
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "rgb(221, 204, 174)";
  //ctx.fillStyle = "palegoldenrod";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  //const c_water = "paleturquoise";
  //const c_bed = "slategrey";
  const c_water = "rgb(190, 219, 215)";
  const c_bed = "rgb(117, 125, 127)";

  const nRivers = 200;
  const rivers = [];

  // Generate river data first
  for (let i = 0; i < nRivers; i++) {
    const depth = Math.floor(random() * (maxDepth - 1)) + 2; // 2–maxDepth
    const start = [random(), 0];
    const end = [10, 4 + random()];
    const river = midpointMeander(start, end, depth, displacement, decay);
    const riverSmooth = chaikinSmoothing(river, 2);
    const width = random() * 10;

    rivers.push({ riverSmooth, depth, width });
  }

  // Determine how many should be water based on probability
  const k = Math.floor(nRivers * prob);

  // Draw first n-k rivers as bed (grey)
  for (let i = 0; i < nRivers - k; i++) {
    const { riverSmooth, width } = rivers[i];
    const alpha = 0.1 + random() * 0.5; // bed alpha
    drawRiver(riverSmooth, c_bed, alpha, width);
  }

  // Draw last k rivers as water (on top)
  for (let i = nRivers - k; i < nRivers; i++) {
    const { riverSmooth, width } = rivers[i];
    const alpha = 1;//0.7 + random() * 0.2; // water alpha
    drawRiver(riverSmooth, c_water, alpha, width);
  }
}


// === UI Controls ===
const dispSlider = document.getElementById("dispSlider");
const decaySlider = document.getElementById("decaySlider");
const probSlider = document.getElementById("probSlider");
const depthSlider = document.getElementById("depthSlider");
const seedInput = document.getElementById("seedInput");
const randomizeBtn = document.getElementById("randomizeBtn");

const dispVal = document.getElementById("dispVal");
const decayVal = document.getElementById("decayVal");
const probVal = document.getElementById("probVal");
const depthVal = document.getElementById("depthVal");

function update() {
  const disp = parseFloat(dispSlider.value);
  const decay = parseFloat(decaySlider.value);
  const prob = parseFloat(probSlider.value);
  const depth = parseInt(depthSlider.value);
  dispVal.textContent = disp.toFixed(2);
  decayVal.textContent = decay.toFixed(2);
  probVal.textContent = prob.toFixed(2);
  depthVal.textContent = depth;
  drawRivers(disp, decay, prob, depth);
}

// When seed input or randomize button changes seed
seedInput.addEventListener("change", () => {
  baseSeed = parseInt(seedInput.value);
  update();
});
randomizeBtn.addEventListener("click", () => {
  baseSeed = Math.floor(Math.random() * 1e9);
  seedInput.value = baseSeed;
  update();
});

// Sliders trigger redraw
[dispSlider, decaySlider, probSlider, depthSlider].forEach(sl => {
  sl.addEventListener("input", update);
});

// Initial draw
update();
</script>


## Further details

Rivers naturally form curves, or [meanders](https://en.wikipedia.org/wiki/Meander){:target="_blank"}, because of the way water flows and interacts with the river banks. When water flows around a slight bend, it moves faster on the outer edge and slower on the inner edge. The faster water erodes the outer bank, while the slower water deposits sediment on the inner bank. This feedback makes the bend grow over time, producing the winding patterns we see in meandering rivers, oxbow lakes, and floodplains.

In our simulation, we mimic this process by repeatedly shifting the midpoint of each river segment in a random perpendicular direction. This models the **instability and sideways migration** of real rivers. Mathematically, the river’s centerline \\(y(x)\\) could be described by a simple equation:

$$
\frac{\partial y}{\partial t} = D \frac{\partial^2 y}{\partial x^2} + \eta(x,t)
$$

Here, \\(D\\) represents smoothing effects like natural sediment spreading, and \\(\eta(x,t)\\) is a random term representing local variations in erosion and deposition.

The **midpoint displacement algorithm** is a simple way to recreate this: each subdivision adds a small random shift, controlled by a displacement parameter \\(p\\) that gets smaller at finer scales (controlled by decay \\(d\\)). After that, **Chaikin’s smoothing** spreads out sharp bends, similar to how real rivers naturally diffuse their curves. Together, these steps create winding, natural-looking river shapes that balance the randomness of erosion with the smoothing effects of sediment redistribution.
