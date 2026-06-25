const API_BASE = 'http://localhost:5000';

const BADGE_COLORS = {
  PHISHING: '#ef4444',
  SUSPICIOUS: '#f59e0b',
  CLEAN: '#10b981',
};

const BADGE_TEXT = {
  PHISHING: '⚠',
  SUSPICIOUS: '?',
  CLEAN: '',
};

async function analyzeUrl(url, tabId) {
  if (!url || url.startsWith('chrome://') || url.startsWith('chrome-extension://')) {
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/api/analyze/url`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
    });

    if (!res.ok) return;

    const data = await res.json();
    const verdict = data.verdict || 'CLEAN';

    await chrome.storage.local.set({
      [`scan_${tabId}`]: {
        url,
        verdict,
        risk_score: data.risk_score,
        confidence: data.confidence,
        scan_id: data.scan_id,
        timestamp: Date.now(),
      },
    });

    chrome.action.setBadgeBackgroundColor({
      color: BADGE_COLORS[verdict] || BADGE_COLORS.CLEAN,
      tabId,
    });
    chrome.action.setBadgeText({
      text: BADGE_TEXT[verdict] || '',
      tabId,
    });
  } catch (err) {
    console.warn('PhishGuard: API unavailable', err.message);
  }
}

chrome.webNavigation.onCompleted.addListener((details) => {
  if (details.frameId !== 0) return;
  analyzeUrl(details.url, details.tabId);
});

chrome.tabs.onActivated.addListener(async (activeInfo) => {
  const stored = await chrome.storage.local.get(`scan_${activeInfo.tabId}`);
  const scan = stored[`scan_${activeInfo.tabId}`];
  if (scan) {
    chrome.action.setBadgeBackgroundColor({
      color: BADGE_COLORS[scan.verdict] || BADGE_COLORS.CLEAN,
      tabId: activeInfo.tabId,
    });
    chrome.action.setBadgeText({
      text: BADGE_TEXT[scan.verdict] || '',
      tabId: activeInfo.tabId,
    });
  }
});
