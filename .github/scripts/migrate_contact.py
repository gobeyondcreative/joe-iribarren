from pathlib import Path
import re
p = Path('index.html')
s = p.read_text()
old = re.search(r"const form = document.getElementById\('contactForm'\);.*?\n// Mobile menu", s, re.S)
if old:
    replacement = '''const form = document.getElementById('contactForm');
const success = document.getElementById('formSuccess');
form.action = 'https://boostconhq.com/api/personal-contact';
const trap = document.createElement('input');
trap.type = 'text'; trap.name = 'website'; trap.tabIndex = -1; trap.autocomplete = 'off';
trap.setAttribute('aria-hidden', 'true');
trap.style.cssText = 'position:absolute;left:-10000px;width:1px;height:1px;overflow:hidden;';
form.appendChild(trap);
const status = document.createElement('p');
status.setAttribute('role', 'status'); status.setAttribute('aria-live', 'polite');
status.style.cssText = 'font-size:14px;line-height:1.6;';
form.appendChild(status);
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const button = form.querySelector('button[type="submit"]');
  if (button.disabled) return;
  const label = button.textContent;
  button.disabled = true; button.textContent = 'Sending...'; status.textContent = '';
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 20000);
  try {
    const response = await fetch(form.action, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(Object.fromEntries(new FormData(form))),
      signal: controller.signal
    });
    const result = await response.json();
    if (!response.ok || result.ok !== true) throw new Error(result.error || 'Your message was not sent. Please try again.');
    form.style.display = 'none'; success.classList.add('show');
  } catch (err) {
    status.textContent = err.name === 'AbortError'
      ? 'Delivery could not be confirmed. Please email joe@boostconhq.com directly to avoid sending twice.'
      : 'Your message could not be sent. Please retry or email joe@boostconhq.com directly.';
  } finally {
    clearTimeout(timeout); button.disabled = false; button.textContent = label;
  }
});

// Mobile menu'''
    s = s[:old.start()] + replacement + s[old.end():]
    s = s.replace('id="contactForm" action="https://formsubmit.co/joe@dealerleadpro.com"', 'id="contactForm" action="https://boostconhq.com/api/personal-contact"')
    s = s.replace('mailto:joe@dealerleadpro.com', 'mailto:joe@boostconhq.com')
    s = s.replace('>joe@dealerleadpro.com<', '>joe@boostconhq.com<')
    p.write_text(s)
    print('Contact form migrated. Newsletter unchanged.')
elif 'const controller = new AbortController();' not in s:
    raise SystemExit('Expected contact handler not found; refusing unsafe edit.')
