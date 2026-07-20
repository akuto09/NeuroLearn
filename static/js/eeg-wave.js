/* NeuroLearn — signature EEG waveform + simulated cognitive metric stream.
   In production these values come from /api/ai/metrics (see ai_engine/). */

function initEegWave(pathId, width, height) {
  const path = document.getElementById(pathId);
  if (!path) return;
  const mid = height / 2;
  let t = 0;

  function buildPath() {
    let d = `M0,${mid}`;
    const points = 60;
    for (let i = 0; i <= points; i++) {
      const x = (width / points) * i;
      const spike = (i % 11 === 0) ? Math.sin(t + i) * (height * 0.32) : 0;
      const noise = Math.sin(i * 0.6 + t * 1.3) * (height * 0.09);
      const y = mid + noise + spike;
      d += ` L${x.toFixed(1)},${y.toFixed(1)}`;
    }
    path.setAttribute('d', d);
  }

  function tick() {
    t += 0.09;
    buildPath();
    requestAnimationFrame(tick);
  }
  tick();
}

function initLiveMetrics(cfg) {
  const state = { attention: 62, meditation: 48, load: 41, fatigue: 22 };
  const colors = {};

  function clamp(v) { return Math.max(4, Math.min(97, v)); }

  function step() {
    state.attention = clamp(state.attention + (Math.random() - 0.5) * 8);
    state.meditation = clamp(state.meditation + (Math.random() - 0.5) * 6);
    state.load = clamp(state.load + (Math.random() - 0.5) * 7);
    state.fatigue = clamp(state.fatigue + (Math.random() - 0.45) * 4);

    Object.keys(cfg).forEach(key => {
      const { val, bar } = cfg[key];
      const valEl = document.getElementById(val);
      const barEl = document.getElementById(bar);
      if (valEl) valEl.textContent = Math.round(state[key]) + '%';
      if (barEl) barEl.style.width = Math.round(state[key]) + '%';
    });
  }
  step();
  setInterval(step, 1400);
}
