const API_BASE = import.meta.env.VITE_API_URL || '';

export async function analyzeUrl(url) {
  const res = await fetch(`${API_BASE}/api/analyze/url`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || 'Analysis failed');
  }
  return res.json();
}

export async function analyzeEmail(emailText) {
  const res = await fetch(`${API_BASE}/api/analyze/email`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email_text: emailText }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || 'Analysis failed');
  }
  return res.json();
}

export async function submitReport(data) {
  const res = await fetch(`${API_BASE}/api/report`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Report submission failed');
  return res.json();
}

export async function getHistory(limit = 50) {
  const res = await fetch(`${API_BASE}/api/history?limit=${limit}`);
  if (!res.ok) throw new Error('Failed to load history');
  return res.json();
}

export async function getStats() {
  const res = await fetch(`${API_BASE}/api/stats`);
  if (!res.ok) throw new Error('Failed to load stats');
  return res.json();
}

export async function getHealth() {
  const res = await fetch(`${API_BASE}/api/health`);
  if (!res.ok) throw new Error('API unavailable');
  return res.json();
}
