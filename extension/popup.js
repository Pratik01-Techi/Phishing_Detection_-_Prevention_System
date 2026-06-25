const API_BASE = 'http://localhost:5000';
const DASHBOARD_URL = 'http://localhost:3000';

const COLORS = { PHISHING: '#ef4444', SUSPICIOUS: '#f59e0b', CLEAN: '#10b981', UNKNOWN: '#94a3b8' };

async function render() {
  const content = document.getElementById('content');
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab?.url) {
    content.innerHTML = '<p class="loading">No active tab</p>';
    return;
  }

  const stored = await chrome.storage.local.get(`scan_${tab.id}`);
  let scan = stored[`scan_${tab.id}`];

  if (!scan || scan.url !== tab.url) {
    try {
      const res = await fetch(`${API_BASE}/api/analyze/url`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: tab.url }),
      });
      if (res.ok) {
        const data = await res.json();
        scan = { url: tab.url, verdict: data.verdict, risk_score: data.risk_score, confidence: data.confidence };
        await chrome.storage.local.set({ [`scan_${tab.id}`]: { ...scan, timestamp: Date.now() } });
      }
    } catch {
      scan = { verdict: 'UNKNOWN', risk_score: 0, confidence: 0 };
    }
  }

  const verdict = scan?.verdict || 'UNKNOWN';
  const score = scan?.risk_score ?? 0;
  const color = COLORS[verdict] || COLORS.UNKNOWN;

  content.innerHTML = `
    <div class="verdict ${verdict}">${verdict}</div>
    <div class="gauge-wrap">
      <div class="gauge" style="--score:${score};--color:${color}">
        <div class="gauge-inner">
          <span class="score" style="color:${color}">${score}</span>
        </div>
      </div>
    </div>
    <div class="meta">
      <p>URL: ${tab.url.slice(0, 45)}${tab.url.length > 45 ? '…' : ''}</p>
      ${scan?.confidence ? `<p>Confidence: ${scan.confidence}%</p>` : ''}
    </div>
    <button class="btn-danger" id="report-btn">Report this site</button>
    <button class="btn-link" id="dashboard-btn">Open Dashboard</button>
  `;

  document.getElementById('report-btn').addEventListener('click', async () => {
    await fetch(`${API_BASE}/api/report`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: tab.url, type: 'phishing', description: 'Reported via extension' }),
    });
    document.getElementById('report-btn').textContent = 'Reported ✓';
  });

  document.getElementById('dashboard-btn').addEventListener('click', () => {
    chrome.tabs.create({ url: DASHBOARD_URL });
  });
}

render();
