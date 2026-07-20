document.addEventListener('DOMContentLoaded', function () {
  initEegWave('dashWavePath', 560, 100);

  function render(metrics) {
    document.getElementById('sAttention').textContent = metrics.attention + '%';
    document.getElementById('sMeditation').textContent = metrics.meditation + '%';
    document.getElementById('sLoad').textContent = metrics.cognitive_load + '%';
    document.getElementById('sFatigue').textContent = metrics.fatigue + '%';
    document.getElementById('barAttention').style.width = metrics.attention + '%';
    document.getElementById('barMeditation').style.width = metrics.meditation + '%';
    document.getElementById('barLoad').style.width = metrics.cognitive_load + '%';
    document.getElementById('barFatigue').style.width = metrics.fatigue + '%';

    const box = document.getElementById('aiRecommendation');
    box.textContent = metrics.recommendation;
    box.className = 'alert mt-24 ' + (
      metrics.status === 'fatigued' ? 'alert-error' :
      metrics.status === 'overloaded' ? 'alert-error' :
      metrics.status === 'focused' ? 'alert-success' : 'alert-info'
    );
  }

  function poll() {
    fetch('/api/ai/metrics')
      .then(r => r.json())
      .then(render)
      .catch(() => {});
  }
  poll();
  setInterval(poll, 4000);
});
