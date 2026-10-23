// IMEI helper: checks the number is typed correctly (15 digits whose last digit is the check digit)
// and prepares the free SMS to 1555, which is the official check. It never says whether a phone is genuine.
export default function ([tool]) {
  const form = tool.querySelector('form');
  const input = tool.querySelector('input');
  const count = tool.querySelector('[data-imei-count]');
  const result = tool.querySelector('[data-imei-result]');
  const sprite = document.querySelector('use')?.getAttribute('href').split('#')[0] || '/assets/icons/sprite.svg';
  const digits = () => input.value.replace(/\D/g, '');

  input.addEventListener('input', () => { count.textContent = `${digits().length} of 15 digits`; });
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const d = digits();
    if (d.length !== 15) show(false, `That is ${d.length} digit${d.length === 1 ? '' : 's'}. An IMEI number has 15 digits: dial *#06# to see yours.`);
    else if (!luhn(d)) show(false, 'The last digit does not match the rest of the number, so it has probably been typed wrongly. Check it against the number shown when you dial *#06#.');
    else show(true, d);
  });

  function show(ok, text) {
    result.hidden = false;
    result.className = `ca-tool__result ${ok ? 'is-ok' : 'is-bad'}`;
    result.innerHTML = ok
      ? `<p><strong>That number is typed correctly.</strong> Now text it to 1555 to find out whether the phone is genuine and which model it is. The SMS is free.</p>
         <div class="ca-actions"><a class="ca-btn ca-btn--primary" href="sms:1555?body=${text}">Text ${text} to 1555<svg class="ca-icon" aria-hidden="true"><use href="${sprite}#arrow-right"/></svg></a></div>
         <p class="ca-hint">On a phone this opens your messages with the number filled in. On a computer, send the 15 digits to 1555 from the phone you are checking.</p>`
      : `<p>${text}</p>`;
  }
}

// IMEI numbers end in a Luhn check digit
function luhn(d) {
  let sum = 0;
  for (let i = 0; i < d.length; i++) {
    let n = +d[d.length - 1 - i];
    if (i % 2) { n *= 2; if (n > 9) n -= 9; }
    sum += n;
  }
  return sum % 10 === 0;
}
