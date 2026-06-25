const BANNER_ID = 'phishguard-warning-banner';

function showWarningBanner() {
  if (document.getElementById(BANNER_ID)) return;

  const banner = document.createElement('div');
  banner.id = BANNER_ID;
  banner.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 2147483647;
    background: #ef4444;
    color: white;
    padding: 12px 20px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    flex-wrap: wrap;
    gap: 8px;
  `;

  banner.innerHTML = `
    <span>🛡️ <strong>PhishGuard:</strong> ⚠️ WARNING — This site has been detected as <strong>PHISHING</strong></span>
    <div style="display:flex;gap:8px;">
      <button id="pg-back" style="background:white;color:#ef4444;border:none;padding:6px 14px;border-radius:6px;cursor:pointer;font-weight:600;">
        ← Go Back
      </button>
      <button id="pg-continue" style="background:transparent;color:white;border:1px solid white;padding:6px 14px;border-radius:6px;cursor:pointer;">
        I understand, continue
      </button>
    </div>
  `;

  document.body.prepend(banner);
  document.body.style.marginTop = '52px';

  document.getElementById('pg-back').addEventListener('click', () => {
    window.history.back();
    banner.remove();
    document.body.style.marginTop = '';
  });

  document.getElementById('pg-continue').addEventListener('click', () => {
    banner.remove();
    document.body.style.marginTop = '';
    sessionStorage.setItem('phishguard_dismissed', 'true');
  });
}

async function checkCurrentPage() {
  if (sessionStorage.getItem('phishguard_dismissed')) return;

  const tabId = await new Promise((resolve) => {
    chrome.runtime.sendMessage({ type: 'getTabId' }, (r) => resolve(r?.tabId));
  }).catch(() => null);

  // Read from storage using tab ID from background
  chrome.storage.local.get(null, (all) => {
    const scans = Object.entries(all).filter(([k]) => k.startsWith('scan_'));
    const latest = scans
      .map(([, v]) => v)
      .filter((v) => v.url === window.location.href)
      .sort((a, b) => b.timestamp - a.timestamp)[0];

    if (latest?.verdict === 'PHISHING') {
      showWarningBanner();
    }
  });
}

checkCurrentPage();

chrome.storage.onChanged.addListener((changes) => {
  for (const [, change] of Object.entries(changes)) {
    if (change.newValue?.url === window.location.href && change.newValue?.verdict === 'PHISHING') {
      showWarningBanner();
    }
  }
});
